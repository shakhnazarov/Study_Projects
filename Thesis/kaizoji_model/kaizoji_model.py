import numpy as np

class KaizojiModel:
    def __init__(self,
        # MODEL
        N_SIMULATIONS = 1000, # number of trading days within one simulation
        N_TRADING_DAYS = 250, # number of trading days in a year

        # ASSETS
        R_F = 0.02, # risk-free return
        D_ZERO = 0.04, # initial dividend
        R_D = 0.04, # mean growth rate of dividends
        STD_D = 0.01, # standard deviation of risky asset's dividend
        P_ZERO = 1,  # initial price of a risky asset
        STD_RISKY_RET = 0.015,  # std of (p_t/p_(t-1) - 1)
        N_RISKY_ASSETS = 1, # number of risky assets
        EXPECT_RISKY_RET = 0.04,  # expectation(p_t/p_(t-1) - 1)

        # NOISY
        FRAC_N_ASSETS_ZERO = 0.3, # initial fraction of risky assets noisy
        W_N_ZERO = 1E4, # initial wealth of noisy
        C_H = 1, # momentum weight
        C_S = 1, # opinion weight
        P_FROM_R_TO_F_ZERO = 0.2, # control probability to switch from risky to free for noisy (2.16 near)
        P_FROM_F_TO_R_ZERO = 0.2,  # control probability to switch from free to risky for noisy (2.16 near)
        MEMORY = 0.95, # memory of noisy investors # near 2.13
        H_ZERO = 0.04, # initial momentum
        N_NOISY_TRADERS = 100, # number of noisy traders in the model

        # COUPLING
        K_ZERO = 0.98 * 0.2, # initial social coupling strength
        MEAN_COUP = 0.98 * 0.2, # Mean of the OU social coupling strength
        ETA_COUP = 0.11, # Mean reversion of the OU social coupling strength #FIXME можно формулу добавить ~70
        STD_COUP = 0.001, # Standard deviation of the OU social coupling strength #FIXME можно формулу добавить ~71

        # FUNDAMENTALISTS
        FRAC_F_ASSETS_ZERO = 0.3, # initial fraction of risky assets fund
        W_F_ZERO = 1E3, # initial wealth of fund
        GAMMA = 1 # parameter in CRRA utility function
        ):

        # MODEL
        self.N_SIMULATIONS = N_SIMULATIONS  # number of trading days within one simulation
        self.N_TRADING_DAYS = N_TRADING_DAYS  # number of trading days in a year

        # ASSETS
        self.R_F = R_F/N_TRADING_DAYS # risk-free return
        self.D_ZERO = D_ZERO/N_TRADING_DAYS # initial dividend
        self.R_D = R_D/N_TRADING_DAYS # mean growth rate of dividends
        self.STD_D = STD_D/np.sqrt(N_TRADING_DAYS) # standard deviation of risky asset's dividend
        self.P_ZERO = P_ZERO  # initial price of a risky asset
        self.STD_RISKY_RET = STD_RISKY_RET/np.sqrt(N_TRADING_DAYS)  # std of (p_t/p_(t-1) - 1)
        self.N_RISKY_ASSETS = N_RISKY_ASSETS # number of risky assets
        self.EXPECT_RISKY_RET = EXPECT_RISKY_RET/N_TRADING_DAYS  # expectation(p_t/p_(t-1) - 1)

        # NOISY
        self.FRAC_N_ASSETS_ZERO = FRAC_N_ASSETS_ZERO # initial fraction of risky assets noisy
        self.W_N_ZERO = W_N_ZERO # initial wealth of noisy
        self.C_H = C_H # momentum weight
        self.C_S = C_S # opinion weight
        self.P_FROM_R_TO_F_ZERO = P_FROM_R_TO_F_ZERO # control probability to switch from risky to free for noisy (2.16 near)
        self.P_FROM_F_TO_R_ZERO = P_FROM_F_TO_R_ZERO  # control probability to switch from free to risky for noisy (2.16 near)
        self.MEMORY = MEMORY # memory of noisy investors # near 2.13
        self.H_ZERO = H_ZERO/N_TRADING_DAYS # initial momentum
        self.N_NOISY_TRADERS = N_NOISY_TRADERS # number of noisy traders in the model

        # COUPLING
        self.K_ZERO = K_ZERO # initial social coupling strength
        self.MEAN_COUP = MEAN_COUP # Mean of the OU social coupling strength
        self.ETA_COUP = ETA_COUP # Mean reversion of the OU social coupling strength
        self. STD_COUP = STD_COUP # Standard deviation of the OU social coupling strength

        # FUNDAMENTALISTS
        self.FRAC_F_ASSETS_ZERO = FRAC_F_ASSETS_ZERO # initial fraction of risky assets fund
        self.W_F_ZERO = W_F_ZERO # initial wealth of fund
        self.GAMMA = GAMMA # parameter in CRRA utility function

        # LOGGING
        self.dividends = [D_ZERO]
        self.fractions_risky_n = [FRAC_N_ASSETS_ZERO]
        self.prices = [P_ZERO]
        self.wealth_f = [W_F_ZERO]
        self.wealth_n = [W_N_ZERO]
        self.fractions_risky_f = [FRAC_F_ASSETS_ZERO]
        self.momentums = [H_ZERO]
        self.couplings = [K_ZERO]
        self.p_free_to_risk_n = [P_FROM_F_TO_R_ZERO]
        self.p_risk_to_free_n = [P_FROM_R_TO_F_ZERO]



        #FIXME del
        self.days = 0


    # MODEL

    def simulate(self, num_simulations = None):
        if num_simulations is None:
            num_simulations = self.N_SIMULATIONS

        for i in range(num_simulations):
            self.next_step()

    def get_variables(self):
        return {
            'dividends': self.dividends,
            'fractions_risky_n': self.fractions_risky_n,
            'prices': self.prices,
            'wealth_f': self.wealth_f,
            'wealth_n': self.wealth_n,
            'fractions_risky_f': self.fractions_risky_f,
            'momentums': self.momentums,
            'couplings': self.couplings,
            'p_free_to_risk_n': self.p_free_to_risk_n,
            'p_risk_to_free_n': self.p_risk_to_free_n
        }

    def next_step(self):
        # set dividends (random variable)
        div_curr = self.dividend_risky(self.dividends[-1])
        self.dividends.append(div_curr)

        # set fractions of risky noisy would want to have
        frac_n_curr = self.frac_noisy_risky(self.fractions_risky_n[-1], self.fractions_risky_n[-1],
                                            self.p_risk_to_free_n[-1], self.p_free_to_risk_n[-1])
        self.fractions_risky_n.append(frac_n_curr)

        # compute price at period t
        price_curr = self.price_level(self.prices[-1], self.wealth_f[-1], self.wealth_n[-1], self.fractions_risky_f[-1],
                                      self.fractions_risky_n[-2], self.fractions_risky_n[-1], self.dividends[-1])
        self.prices.append(price_curr)

        # compute current capital return (excluding dividends)
        cap_ret_curr = self.capital_return(self.prices[-1], self.prices[-2])

        # compute current excessive return
        excess_ret_curr = self.excess_return(cap_ret_curr, self.dividends[-1], self.prices[-2])

        # compute current wealth of fundamental investor
        wealth_fund_curr = self.wealth_fund(excess_ret_curr, self.fractions_risky_f[-1], self.wealth_f[-1])
        self.wealth_f.append(wealth_fund_curr)

        # compute current wealth of noisy investors
        wealth_noisy_surr = self.wealth_noisy(excess_ret_curr, self.fractions_risky_n[-2], self.wealth_n[-1])
        self.wealth_n.append(wealth_noisy_surr)

        # compute current fraction of wealth in risky for fundamentalist
        frac_f_curr = self.frac_fund_risky(self.dividends[-1], self.prices[-1])
        self.fractions_risky_f.append(frac_f_curr)

        # compute current price momentum
        moment_curr = self.price_momentum(self.momentums[-1], cap_ret_curr)
        self.momentums.append(moment_curr)

        # compute current coupling strength
        k_curr = self.k_coupling_strength(self.couplings[-1])
        self.couplings.append(k_curr)

        # compute current opinion
        opinion_curr = self.opinion(self.fractions_risky_n[-1])

        # compute current probability to switch from free to risky for noisy
        f_to_r_n_curr = self.from_f_to_r(opinion_curr, self.momentums[-1], self.couplings[-1])
        self.p_free_to_risk_n.append(f_to_r_n_curr)

        # compute current probability to switch from risky to free for noisy
        r_to_f_n_curr = self.from_r_to_f(opinion_curr, self.momentums[-1], self.couplings[-1])
        self.p_risk_to_free_n.append(r_to_f_n_curr)



# <------------------------------------------------------------------------------------------------------>

    # INVESTMENT UNIVERSE
    def dividend_risky(self, prev_value):
        return prev_value * (1 + np.random.normal(self.R_D, self.STD_D))  # FIXME нужно только один раз вызывать, потому что случайно

    def price_level(self, prev_price, prev_w_f, prev_w_n, prev_frac_f, prev_frac_n, frac_n, div):
        aux_exc = (self.EXPECT_RISKY_RET - self.R_F) / (self.GAMMA * np.power(self.STD_RISKY_RET, 2))
        aux_free_div = prev_frac_f * (-1 + div / prev_price - self.R_F) + self.R_F + 1
        aux_div = div*(1+self.R_D) / (self.GAMMA * np.power(self.STD_RISKY_RET, 2))
        a_f = 1/prev_price * prev_w_f  * prev_frac_f * (aux_exc - 1)
        b_f = prev_w_f * (aux_exc * aux_free_div + aux_div * prev_frac_f / prev_price)
        c_f = prev_w_f * aux_div * aux_free_div
        a_n = 1/prev_price * prev_w_n *  prev_frac_n * (frac_n - 1)
        b_n = prev_w_n * frac_n * (prev_frac_n * (-1 + div / prev_price - self.R_F) + self.R_F + 1)
        c_n = 0

        a = a_n + a_f
        b = b_n + b_f
        c = c_n + c_f

        # print('DAY', self.days)
        # print('a_f', a_f)
        # print('b_f', b_f)
        # print('c_f', c_f)
        # print('a_n', a_n)
        # print('b_n', b_n)
        # print('c_n', c_n)
        # print('aux_exc', aux_exc)
        # print('aux_free_div', aux_free_div)
        # print('aux_div', aux_div)
        # print('<----------------------------------------------------------------->')
        self.days += 1
        return max((-1*b + np.sqrt(np.power(b,2) - 4*a*c))/(2*a), (-1*b - np.sqrt(np.power(b,2) - 4*a*c))/(2*a))

    def capital_return(self, price, prev_price): # ~3
        return price/prev_price - 1

    def excess_return(self, cap_return, dividend, prev_price):  #FIXME возможно стоит использовать expected (2.4) ~5
        return cap_return + dividend/prev_price - self.R_F


    # FUNDAMENTALISTS
    def utility_fund(self, wealth): # CRRA ~7
        if self.GAMMA == 1:
            return np.log(wealth)
        else:
            return np.power(wealth, 1-self.GAMMA)/(1-self.GAMMA)

    #
    # def fund_price_t(self, t):  # 2.7
    #     return self.P_ZERO * np.power(1+self.EXPECT_RISKY_RET, t)

    def frac_fund_risky(self, dividend, price):  # 2.8 ~13
        return (self.EXPECT_RISKY_RET + dividend * (1 + self.R_D) / price - self.R_F)/(self.GAMMA * np.power(self.STD_RISKY_RET, 2))

    def wealth_fund(self, excess_ret, prev_frac, prev_wealth):  # 2.10 ~4 (in ~ there is a difference of wealth)
        return excess_ret*prev_wealth*prev_frac + prev_wealth * (1+self.R_F)

    def excess_demand_fund(self, wealth, prev_wealth, share, prev_share, price, prev_price):  # 2.11 ~16 но другие изменения
        return share*wealth - prev_share * prev_wealth * price / prev_price



    # NOISY TRADERS
    def opinion(self, frac_risk_n):  # 2.12 ~ 28
        return 2*frac_risk_n - 1

    def price_momentum(self, prev_p_m, cap_ret):  # 2.13
        return self.MEMORY * prev_p_m + (1-self.MEMORY)*cap_ret

    def from_r_to_f(self, opin, p_m, k):  # 2.16  FIXME разные формулы в статьях
        return self.P_FROM_R_TO_F_ZERO / 2 * (1-k*(opin + p_m))

    def from_f_to_r(self, opin, p_m, k):  # 2.16 FIXME разные формулы в статьях
        return self.P_FROM_F_TO_R_ZERO / 2 * (1+k*(opin + p_m))

    def k_coupling_strength(self, prev_k):  # 2.17
        return prev_k + self.ETA_COUP * (self.MEAN_COUP - prev_k) + self.STD_COUP*np.random.standard_normal()

    def frac_noisy_risky(self, risky_n_prev, free_n_prev, p_r_to_f_prev, p_f_to_r_prev):  # 2.20 FIXME использовал прошлые N, нцжно првоерить что суммируется в 1000
        sum_1 = 0
        sum_2 = 0
        num_r = int(risky_n_prev * self.N_NOISY_TRADERS)
        num_f = self.N_NOISY_TRADERS - num_r
        for i in range(num_r):
            sum_1 += 1 - np.random.binomial(n=1, p=p_r_to_f_prev) # Bernoulli prob #FIXME можно binomial сразу
        for i in range(num_f):
            sum_1 += np.random.binomial(n=1, p=p_f_to_r_prev)

        return 1/(num_r + num_f) * (sum_1 + sum_2)

    def wealth_noisy(self, excess_ret, prev_frac, prev_wealth):  # 2.21
        return excess_ret*prev_wealth*prev_frac + prev_wealth * (1+self.R_F)

    def excess_demand_noisy(self, wealth, prev_wealth, share, prev_share, price, prev_price):  # 2.22
        return share*wealth - prev_share * prev_wealth * price / prev_price








#FIXME check by
# :In our simulations, we verify that the long-term growth rate of prices is equal to the average
# growth rate rd of dividends, as defined in expression
# seed добавить



