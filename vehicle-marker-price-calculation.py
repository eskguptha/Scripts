__author__ = 'Santhosh Emmadi'
"""
https://github.com/eskguptha
Python Version : 3
cd folder
python saved.py
"""
import os
import logging
from logging import handlers
from datetime import datetime

LOG_ROTATE = 'midnight'
if not os.path.exists('logs'):
    os.makedirs('logs')
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
log_level = logging.DEBUG

LOG_FILE = os.path.join('logs', 'program.log')
handler = handlers.TimedRotatingFileHandler(LOG_FILE, when=LOG_ROTATE)
handler.setFormatter(formatter)
logger = logging.getLogger("program")
logger.addHandler(handler)
logger.setLevel(log_level)


# Category wise Vechicle Market Price Ranges
ENGINE_MARKET_PRICE_RANGE = [
    {"category_name": "category A", "value": ((0, 1600),  25)},
    {"category_name": "category B", "value": ((1601, 2000),  50)},
    {"category_name": "category C", "value": ((2001, float("inf")),  75)}
]

# Maximum depreciation allowed per vehicle
MAXIMUM_DEPRECIATION_ALLOWED = 10

# Vehicle depreciation per Year
DEPRECIATION_PER_YEAR = 1

# User Intput Questions
QUESTION_LIST = (
    ('market_price', 'Enter the market price: '),
    ('engine_capacity', 'Enter the engine capacity: '),
    ('manufacture_year', 'Enter the manufacture year: ')
)


class UCAVehicleMarketSalesAlg():
    """
    Utopia Customs Authority has employed you to 
    develop an application to help their customers 
    calculate the customs for imported vehicles

    Input : 
           market_price(integer)
           engine_capacity(integer)
           manufacture_year(integer)
    Output : 
            Initial customs amount ($Category Number): $Number
            Depreciation discount ($Number years): $Number
            Final customs amount: $Number
    """

    def __init__(self, **kwargs):
        self.market_price = kwargs.get('market_price')
        self.engine_capacity = kwargs.get('engine_capacity')
        self.manufacture_year = kwargs.get('manufacture_year')
        self.category_name = None
        self.customs_amount = None
        self.depreciation_discount = None
        self.final_customs_amount = None
        self.depreciation_discount_in_yrs = None
        self.logger = logger
        self.errors_list = []

    def Validate(self, data):
        """
        Validating the Inputdata
        """
        self.logger.info('getEngineMarketPricePercent start {}'.format(data))
        for key, value in data.items():
            try:
                value = int(value)
                if value <= 0:
                    self.errors_list.append(f"{key} value must > 0 Only")
            except ValueError as e:
                self.logger.info('Validate Exception : {}'.format(e))
                self.errors_list.append(f"{key} value must number Only")
            except TypeError as e:
                self.errors_list.append(f"{key} value must required")
                self.logger.info('Validate Exception : {}'.format(e))
        self.logger.info(
            'getEngineMarketPricePercent End {}'.format(self.errors_list))
        pass

    def getPercentAmount(self, expression):
        """
        Calculating Percentage from expression
        """
        self.logger.info('getPercentAmount start')
        if "%" in expression:
            expression = expression.replace("%", "/100")
        expression_val = eval(expression)
        self.logger.info('getPercentAmount End {}'.format(expression_val))
        return expression_val

    def getEngineMarketPricePercent(self):
        """
        Get Engine Market Price Percentage from avaialble categories with cc range
        """
        self.logger.info('getEngineMarketPricePercent start')
        engine_market_price_percent = 0
        category_name = None
        for idx, each_category in enumerate(ENGINE_MARKET_PRICE_RANGE):
            cc_start_range, cc_end_range = each_category['value'][0]
            if self.engine_capacity >= cc_start_range and len(ENGINE_MARKET_PRICE_RANGE) == idx+1:
                return each_category['category_name'], each_category['value'][1]
            elif self.engine_capacity >= cc_start_range and self.engine_capacity <= cc_end_range:
                return each_category['category_name'], each_category['value'][1]
            

        self.logger.info('getEngineMarketPricePercent End : Category : {} Percentage: {}'.format(
            category_name, engine_market_price_percent))
        return category_name, engine_market_price_percent

    def getDepreciationDiscountPercent(self):
        """
        Calculate Depreciation Discount Percentage from requested vechicle manfacture year
        """
        self.logger.info('getDepreciationDiscountPercent start')
        depreciation_discount_diff = datetime.now().year - self.manufacture_year
        if depreciation_discount_diff > 0 and depreciation_discount_diff <= MAXIMUM_DEPRECIATION_ALLOWED:
            depr_disc_percent = int(
                float(depreciation_discount_diff) * float(DEPRECIATION_PER_YEAR))
        elif depreciation_discount_diff > MAXIMUM_DEPRECIATION_ALLOWED:
            depr_disc_percent = MAXIMUM_DEPRECIATION_ALLOWED
        else:
            depr_disc_percent = 0
        self.logger.info('getDepreciationDiscountPercent End : Depreciation in Yrs : {} Percentage: {}'.format(
            depreciation_discount_diff, depr_disc_percent))
        return depreciation_discount_diff, depr_disc_percent

    def calculatePrice(self):
        """
        Calculate Vehicle Market Value Price 
        """
        self.Validate({
            "Market Price": self.market_price,
            "Engine Capacity": self.engine_capacity,
            "Manufacture Year": self.manufacture_year
        })
        if len(self.errors_list) == 0:
            self.logger.info('calculatePrice start')
            try:
                self.category_name, engine_market_price_percent = self.getEngineMarketPricePercent()
                self.customs_amount = self.getPercentAmount(
                    f"{self.market_price}*{engine_market_price_percent}%")
                self.depreciation_discount_in_yrs, depr_disc_percent = self.getDepreciationDiscountPercent()
                self.depreciation_discount = self.getPercentAmount(
                    f"{self.market_price}*{depr_disc_percent}%")
                self.final_customs_amount = self.customs_amount - self.depreciation_discount
            except (ValueError, TypeError) as e:
                self.logger.info('calculatePrice Exception : {}'.format(e))
                self.errors_list.append('calculatePrice : program Error')
                pass
            self.logger.info('calculatePrice End')
        self.display_data()
        pass

    def display_data(self):
        """
        print output data from calculatePrice method
        """
        self.logger.info('display_data Start')
        if len(self.errors_list) > 0:
            for each_error in self.errors_list:
                print(each_error)
        else:
            print('Initial customs amount ({}): ${:,.0f}'.format(
                self.category_name, self.customs_amount))
            print('Depreciation discount ({} year{}): ${:,.0f}'.format(
                f'{MAXIMUM_DEPRECIATION_ALLOWED}+' if self.depreciation_discount_in_yrs > MAXIMUM_DEPRECIATION_ALLOWED else self.depreciation_discount_in_yrs,
                's'if self.depreciation_discount_in_yrs > 0 else '',
                self.depreciation_discount))
            print('Final customs amount: ${:,.0f}'.format(
                self.final_customs_amount))
        self.logger.info('display_data End')
        pass


def getQuestions(each_question_name, each_question_text):
    """
    Collect Answers from User Input
    """
    while True:
        try:
            value = int(input(each_question_text))
            if value < 0:
                print("Please input greater than 0 only...")
                continue
            break
        except ValueError as e:
            logger.info('getQuestions Exception : {}'.format(e))
            print("Please input integer only...")
            continue
    return value


def main():
    """
    Prepare Question and Answers to get vehicle market price from UCAVehicleMarketSalesAlg
    """
    i = 0
    while True:
        if i == 0:
            print('Utopia Vehicle Customs Calculator')
            print('-'*33)
        answer_data = {}
        for each_question_name, each_question_text in QUESTION_LIST:
            answer_data[each_question_name] = getQuestions(
                each_question_name, each_question_text)
        ucavms_cls_obj = UCAVehicleMarketSalesAlg(**answer_data)
        print('\n')
        ucavms_cls_obj.calculatePrice()
        print('\n')
        answer = input('Calculate for another vehicle (y/n)? ')
        if answer.lower() == 'n':
            print('Have a nice day!')
            break
        elif answer.lower() == 'y':
            print('\n')
            continue
        else:
            print("Invalid Option Entered")
            break
        i = +1


if __name__ == '__main__':
    main()
