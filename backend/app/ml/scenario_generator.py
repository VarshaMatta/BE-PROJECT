import numpy as np
from typing import List

class ScenarioGenerator:
    @staticmethod
    def generate_candidate_prices(min_price: float, max_price: float, current_price: float, num_steps: int = 10) -> List[float]:
        """
        Generates candidate price points uniformly spaced between min_price and max_price,
        ensuring current_price is included if within range.
        """
        if min_price > max_price:
            return []
        
        if min_price == max_price:
            return [round(min_price, 2)]

        prices = list(np.linspace(min_price, max_price, num_steps))
        if current_price >= min_price and current_price <= max_price:
            prices.append(current_price)
        
        # Round to 2 decimal places and deduplicate
        prices = sorted(list(set([round(p, 2) for p in prices])))
        return prices
