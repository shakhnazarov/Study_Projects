import mesa

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(x_i * (N-i) for i, x_i in enumerate(x)) / (N * sum(x))
    return 1 + (1/N) - 2*B
# Create an agent
class MoneyAgent(mesa.Agent):
    """An agent with fixed amount of initial money"""

    def __init__(self, unique_id, model):
        # pass parameters to the parent class
        super().__init__(unique_id, model)
        # initial wealth
        self.wealth = 1

    # move to the neighbor
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore = True,
            include_center = False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    # give money to the same cell
    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        # inherent list of agents in the scheduler
        self.move()
        if self.wealth > 0:
            self.give_money()

# Create a modeler with scheduler and data_collector
class MoneyModel(mesa.Model):
    """A model with some number of agents"""

    def __init__(self, N, width, height):
        self.num_agents = N
        # create procedure by which agents act
        self.schedule = mesa.time.RandomActivation(self)
        # add spatial element
        self.grid = mesa.space.MultiGrid(width, height, True)

        # create agents
        for i in range(self.num_agents):
            ag = MoneyAgent(i, self)
            self.schedule.add(ag)

            # place agent on a random grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(ag, (x,y))

        # collect data for model
        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        )


    def step(self):
        """Advance the model by one step"""
        self.datacollector.collect(self)
        # make step of each agent
        self.schedule.step()




