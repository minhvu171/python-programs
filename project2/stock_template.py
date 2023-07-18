"""

Name:      Minh Vu
Email:     minh.vu@tuni.fi

This program executes commands related to the inventory of
a warehouse that contains many objects of type "Product".
Depending on the command, the program would either print out
the products or modify the products' characteristic. All the
commands are:
1. print: Print out the information of all the products
2. print <code>: Prints the information of the product specified by the code
3. change <code> <amount>: Changes the inventory amount of the product indicated
by the code by the amount
4. delete <code>: Deletes the product identified by the code
5. low: Prints all products in ascending order by product code whose inventory
quantity has fallen below a preset limit.
6. combine <code₁> <code₂>: Combines 2 products into 1
7. sale <category> <sale_percentage>: set a sale price for all the products in
a specific category.

"""


LOW_STOCK_LIMIT = 30


class Product:
    """
    This class represent a product i.e. an item available for sale.
    """

    def __init__(self, code, name, category, price, stock):
        self.__code = code
        self.__name = name
        self.__category = category
        self.__price = price
        self.__stock = stock
        self.__original_price = price  # only need when calculating the sale price

    def get_stock(self):
        """
        fetch the stock size
        :return: the stock size
        """

        return self.__stock

    def get_price(self):
        """
        fetch the price
        :return: the price
        """

        return self.__price

    def get_category(self):
        """
        fetch the category
        :return: the category
        """

        return self.__category

    def __str__(self):
        """
        An already provided function
        """

        lines = [
            f"Code:     {self.__code}",
            f"Name:     {self.__name}",
            f"Category: {self.__category}",
            f"Price:    {self.__price:.2f}€",
            f"Stock:    {self.__stock} units",
        ]

        longest_line = len(max(lines, key=len))

        for i in range(len(lines)):
            lines[i] = f"| {lines[i]:{longest_line}} |"

        solid_line = "+" + "-" * (longest_line + 2) + "+"
        lines.insert(0, solid_line)
        lines.append(solid_line)

        return "\n".join(lines)

    def __eq__(self, other):
        """
        An already provided function
        """

        return self.__code == other.__code and \
               self.__name == other.__name and \
               self.__category == other.__category and \
               self.__price == other.__price

    def modify_stock_size(self, amount):
        """

        Allows the <amount> of items in stock to be modified.
        This is a very simple method: it does not check the
        value of <amount> which could possibly lead to
        a negative amount of items in stock. Caveat emptor.

        :param amount: int, how much to change the amount in stock.
                       Both positive and negative values are accepted:
                       positive value increases the stock and vice versa.
        """

        self.__stock += amount

    def belong_to_category(self, category):
        """
        Check if the product belongs to a specific category or not.
        This method is utilized in the sale_command (to set the sale price
        for all products that belong to a category) and also in the
        can_combine method below (to check if 2 products are of the same
        category or not).

        :param Any, category: the target category .
        :return: True, if the product belongs to that category.
        :return: False, if the product doesn't belong to that category
        """
        if self.__category == category:
            return True
        else:
            return False

    def sale_price(self, sale):
        """
        Calculate the sale price for a product based on its
        original price. This method is utilized in the sale_command

        :param sale: float, how much the price will be put on sale
        """
        self.__price = self.__original_price*(100-sale)/100

    def same_price(self, product):
        """
        Check if two products are of the same price or not. This method is
        utilized in the combine_command.
        :param product: Product, the target product whose price will be
        compared.

        :return: True, if two products have the same price | False,
        if two products don't have the same price
        """

        if self.get_price() == product.get_price():
            return True
        else:
            return False

    def can_combine(self, product):
        """
        Check if two products can be combined into one or not. If yes, then add the
        target product's stock size to the self stock size. This method is utilized
        in the combine_command.

        :param product: Product, the target product that will be checked
        :return: True, if two products can be combined | False, if two products
        can't be combined
        """

        if not self.belong_to_category(product.get_category()):
            print(f"Error: combining items of different categories '{self.get_category()}' and "
                  f"'{product.get_category()}'.")
            return False
        elif not self.same_price(product):
            print(f"Error: combining items with different prices {self.get_price()}€ and {product.get_price()}€.")
            return False
        else:
            self.modify_stock_size(product.get_stock())
            return True

    def can_be_deleted(self):
        """
        Check if a product can be deleted from the warehouse or not. This
        method is utilized in the delete_command
        :return: True, if it can be deleted | False, if it can't be deleted
        """

        if self.get_stock() > 0:
            return False
        else:
            return True

    def is_low(self):
        """
        Check if the stock size is below the preset limit or not.
        This method is utilized in the low_command.

        :return: True, if the stock size is below the limit | False, if
        the stock size isn't below the limit
        """

        if self.get_stock() < LOW_STOCK_LIMIT:
            return True
        else:
            return False


def _read_lines_until(fd, last_line):
    """

    Reads lines from <fd> until the <last_line> is found.
    Returns a list of all the lines before the <last_line>
    which is not included in the list. Return None if
    file ends bofore <last_line> is found.
    Skips empty lines and comments (i.e. characeter '#'
    and everything after it on a line).

    You don't need to understand this function works as it is
    only used as a helper function for the read_database function.

    :param fd: file, file descriptor the input is read from.
    :param last_line: str, reads lines until <last_line> is found.
    :return: list[str] | None
    """

    lines = []

    while True:
        line = fd.readline()

        if line == "":
            return None

        hashtag_position = line.find("#")
        if hashtag_position != -1:
            line = line[:hashtag_position]

        line = line.strip()

        if line == "":
            continue

        elif line == last_line:
            return lines

        else:
            lines.append(line)


def read_database(filename):
    """

    This function reads an input file which must be in the format
    explained in the assignment. Returns a dict containing
    the product code as the key and the corresponding Product
    object as the payload. If an error happens, the return value will be None.

    :param filename: str, name of the file to be read.
    :return: dict[int, Product] | None
    """

    data = {}

    try:
        with open(filename, mode="r", encoding="utf-8") as fd:

            while True:
                lines = _read_lines_until(fd, "BEGIN PRODUCT")
                if lines is None:
                    return data

                lines = _read_lines_until(fd, "END PRODUCT")
                if lines is None:
                    print(f"Error: premature end of file while reading '{filename}'.")
                    return None

                # print(f"TEST: {lines=}")

                collected_product_info = {}

                for line in lines:
                    keyword, value = line.split(maxsplit=1)  # ValueError possible

                    # print(f"TEST: {keyword=} {value=}")

                    if keyword in ("CODE", "STOCK"):
                        value = int(value)  # ValueError possible

                    elif keyword in ("NAME", "CATEGORY"):
                        pass  # No conversion is required for string values.

                    elif keyword == "PRICE":
                        value = float(value)  # ValueError possible

                    else:
                        print(f"Error: an unknown data identifier '{keyword}'.")
                        return None

                    collected_product_info[keyword] = value

                if len(collected_product_info) < 5:
                    print(f"Error: a product block is missing one or more data lines.")
                    return None

                product_code = collected_product_info["CODE"]
                product_name = collected_product_info["NAME"]
                product_category = collected_product_info["CATEGORY"]
                product_price = collected_product_info["PRICE"]
                product_stock = collected_product_info["STOCK"]

                product = Product(code=product_code,
                                  name=product_name,
                                  category=product_category,
                                  price=product_price,
                                  stock=product_stock)

                # print(product)

                if product_code in data:
                    if product == data[product_code]:
                        data[product_code].modify_stock_size(product_stock)

                    else:
                        print(f"Error: product code '{product_code}' conflicting data.")
                        return None

                else:
                    data[product_code] = product

    except OSError:
        print(f"Error: opening the file '{filename}' failed.")
        return None

    except ValueError:
        print(f"Error: something wrong on line '{line}'.")
        return None


def delete_command(warehouse, parameters):
    """
    This function executes the "delete" command that deletes an
    existing product with the stock size <= 0

    :param warehouse: dict[int, Product], dict of all known products.
    :param parameters: str, parameter of the command.
    """
    try:
        code = int(parameters)
    except ValueError:
        print(f"Error: product \'{parameters}\' can not be deleted as it does not exist.")
        return

    if code not in warehouse:
        print(f"Error: product \'{code}\' can not be deleted as it does not exist.")
    else:
        if not warehouse[code].can_be_deleted():
            print(f"Error: product \'{parameters}\' can not be deleted as stock remains.")
        else:
            del warehouse[code]


def changes_command(warehouse, parameters):
    """
    This function execute the "change" command that changes the stock
    size of a product

    :param warehouse: dict[int, Product], dict of all known products.
    :param parameters: str, parameter of the command.
    """

    try:
        # Splitting the <parameters> string into two parts.
        # Raises ValueError if there are more or less than exactly two
        # values in the <parameters> string.
        code, amount = parameters.split()

        # First parameter was supposed to be a products code i.e. an integer
        # and the second should be an integer. If either of these assumptions fail
        # ValueError will be raised.
        code = int(code)
        amount = int(amount)

    except ValueError:
        print(f"Error: bad parameters '{parameters}' for change command.")
        return

    # <code> should be an existing product code in the <warehouse>.
    if code not in warehouse:
        print(f"Error: stock for '{code}' can not be changed as it does not exist.")
    else:
        warehouse[code].modify_stock_size(amount)


def low_command(warehouse):
    """
    This function execute the "low" command that prints the products that have
    the stock size below the preset limit

    :param warehouse: dict[int, Product], dict of all known products.
    """

    # create a dictionary that contains the products with low stock size
    low_product = {}
    for product_code in warehouse:
        # product is the code
        if warehouse[product_code].is_low():
            low_product[product_code] = warehouse[product_code]
        else:
            continue

    # now the low_product dictionary should contain all the products with low stock size
    for product in sorted(low_product):
        print(low_product[product].__str__())


def combine_command(warehouse, parameter):
    """
    This function execute the "combine" command that combines 2 products
    into one.

    :param warehouse: dict[int, Product], dict of all known products.
    :param parameter: str, parameter of the command
    """

    # checking if the input is valid or not
    try:
        code1, code2 = parameter.split()
        code1 = int(code1)
        code2 = int(code2)

    except ValueError:
        if len(parameter.split()) != 2:
            print(f"Error: bad command line 'combine {parameter}'.")
            return
        else:
            print(f"Error: bad parameters '{parameter}' for combine command.")
            return

    # the user has entered the correct amount of integer parameters.
    # Now check if both codes exist or code1 is the same as code 2 or not
    if code1 not in warehouse or code2 not in warehouse or code1 == code2:
        print(f"Error: bad parameters '{parameter}' for combine command.")
        return

    # Now check if two products can be combined or not
    if warehouse[code1].can_combine(warehouse[code2]):
        del warehouse[code2]
    else:
        pass


def sale_command(warehouse, parameter):
    """
    This function execute the "sale" command that set the price of
    the products that belong to a category to the sale price.

    :param warehouse: dict[int, Product], dict of all known products.
    :param parameter: str, parameter of the command
    """

    # checking the validity of the input
    try:
        category, sale = parameter.split()
        sale = float(sale)
    except ValueError:
        print(f"Error: bad parameters '{parameter}' for sale command.")
        return

    # Firstly, find the occurrences of the category in the warehouse.
    # Create a list of product to be sale.
    # Set the occurrences of this category to 0.
    product_to_be_sale = []
    occurrences_of_category = 0
    for product_code in warehouse:
        if warehouse[product_code].belong_to_category(category):
            occurrences_of_category += 1
            product_to_be_sale.append(warehouse[product_code])
        else:
            continue

    # Now, we know the occurrence of this category, if it's greater
    # than 0, we execute the sale_price method to the products in the
    # product_to_sale list
    if occurrences_of_category == 0:
        print(f"Sale price set for 0 items.")
    else:
        print(f"Sale price set for {occurrences_of_category} items.")
        for product in product_to_be_sale:
            product.sale_price(sale)


def print_a_product_command(warehouse, parameter):
    """
    This function execute the "print <code>" command that print a specific
    product

    :param warehouse: dict[int, Product], dict of all known products.
    :param parameter: str, parameter of the command
    """
    try:
        code = int(parameter)
    except ValueError:
        print(f"Error: product \'{parameter}\' can not be printed as it does not exist.")
        return

    if code in warehouse:
        print(warehouse[code].__str__())
    else:
        print(f"Error: product \'{parameter}\' can not be printed as it does not exist.")


def main():
    filename = input("Enter database name: ")

    warehouse = read_database(filename)
    if warehouse is None:
        return

    while True:
        command_line = input("Enter command: ").strip()

        if command_line == "":
            return

        command, *parameters = command_line.split(maxsplit=1)

        command = command.lower()

        if len(parameters) == 0:
            parameters = ""
        else:
            parameters = parameters[0]

        if "print".startswith(command) and parameters == "":
            for product in sorted(warehouse):
                print(warehouse[product].__str__())

        elif "print".startswith(command) and parameters != "":
            print_a_product_command(warehouse, parameters)

        elif "delete".startswith(command) and parameters != "":
            delete_command(warehouse, parameters)

        elif "change".startswith(command) and parameters != "":
            changes_command(warehouse, parameters)

        elif "low".startswith(command) and parameters == "":
            low_command(warehouse)

        elif "combine".startswith(command) and parameters != "":
            combine_command(warehouse, parameters)

        elif "sale".startswith(command) and parameters != "":
            sale_command(warehouse, parameters)

        else:
            print(f"Error: bad command line '{command_line}'.")


if __name__ == "__main__":
    main()
