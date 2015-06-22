"""
Cookie Clicker Simulator
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._cookies_persecond = 1.0
        self._item_name = ""
        self._item_cost = 0.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Time: " + str(self._current_time) + \
               " Current Cookies: " + str(self._current_cookies) + \
               " CPS: "+str(self._cookies_persecond) + \
               " Total Cookies: " + str(self._total_cookies) + \
               " History (length: " + str(len(self._history)) + "): " + str(self._history)

    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cookies_persecond
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history
        
    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """      
        if cookies >= self._current_cookies:
            real_time = (cookies - self._current_cookies) / self._cookies_persecond
            if real_time % 1 != 0:
                return real_time - real_time%1 +1
            else:
                return real_time
        else:
            return 0.0
        
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._current_time += time
            self._current_cookies += self._cookies_persecond * time
            self._total_cookies += self._cookies_persecond * time 
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._item_name = item_name
            self._item_cost = cost
            self._cookies_persecond += additional_cps
            self._current_cookies -= cost
            self._history.append((self._current_time, self._item_name, self._item_cost, self._total_cookies))
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    clickerstatenew = ClickerState()
    new_buildinfo = build_info.clone()
    
    while clickerstatenew.get_time() <= duration:
        item = strategy(clickerstatenew.get_cookies(), clickerstatenew.get_cps(), 
                        duration - clickerstatenew.get_time(), new_buildinfo)
        #print item
        if item == None:
            break
        else:       
            wait_time = clickerstatenew.time_until(new_buildinfo.get_cost(item))
            if clickerstatenew.get_time() + wait_time > duration:
                break
            else:
                clickerstatenew.wait(wait_time)
                clickerstatenew.buy_item(item, new_buildinfo.get_cost(item), new_buildinfo.get_cps(item))
                new_buildinfo.update_item(item)
        
    clickerstatenew.wait(duration - clickerstatenew.get_time())   
    return clickerstatenew


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    this strategy should always select the cheapest item that you can afford in the time left
    """
    cheapest_cost = float('inf')
    build_items = build_info.build_items()   
    for item in build_items:
        if build_info.get_cost(item) <= cheapest_cost:
            cheapest_cost = build_info.get_cost(item)            
            cheapest_item = item          
    if cheapest_cost > (time_left * cps + cookies):
        return None
    else:
        return cheapest_item

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    this strategy should always select the most expensive item you can afford in the time left
    """
    highest_cost = float('-inf')
    build_items = build_info.build_items()   
    for item in build_items:
        if build_info.get_cost(item) >= highest_cost and build_info.get_cost(item) <= (time_left * cps + cookies):
            highest_cost = build_info.get_cost(item)            
            highest_item = item
    if highest_cost == float('-inf'):
        return None
    else:
        return highest_item

def strategy_best(cookies, cps, time_left, build_info):
    """
    this is the best strategy 
    """
    highest_ratio = float('-inf')
    build_items = build_info.build_items()   
    for item in build_items:
        if (build_info.get_cps(item) / build_info.get_cost(item) >= highest_ratio) and \
           (build_info.get_cost(item) <= (time_left * cps + cookies)):
            highest_ratio = build_info.get_cps(item) / build_info.get_cost(item)            
            highest_item = item
    if highest_ratio == float('-inf'):
        return None
    else:
        return highest_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_best)
    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
