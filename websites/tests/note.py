from websites.models import Websites, Categories, Products, Groups, Options

website = Websites.objects.create(url='website', title="Website Test")
category = Categories.objects.create(websites=website, title="Category 1")
Categories.objects.create(websites=website, title="Category 2")
Categories.objects.create(websites=website, title="Category 3")
Categories.objects.create(websites=website, title="Category 4")


product1 = Products.objects.create(websites=website, categories=category, title='Price type 1',
                                   price=30000, price_type='1')
product2 = Products.objects.create(websites=website, categories=category, title='Price type 2',
                                   price=30000, price_type='2')
product3 = Products.objects.create(websites=website, categories=category, title='Price type 3',
                                   price_type='3')

radio = Groups.objects.create(websites=website, products=product1, title="radio", maximum=1, minimum=1)
checkbox = Groups.objects.create(websites=website, products=product1, title="checkbox", maximum=1, minimum=0)
numbers = Groups.objects.create(websites=website, products=product1, title="numbers", maximum=10, minimum=0)

Options.objects.create(websites=website, groups=radio, title="Op1")
Options.objects.create(websites=website, groups=radio, title="Op2")
Options.objects.create(websites=website, groups=radio, title="Op3")
Options.objects.create(websites=website, groups=radio, title="Readonly", maximum=1, minimum=1)

Options.objects.create(websites=website, groups=checkbox, title="Op1")
Options.objects.create(websites=website, groups=checkbox, title="Op2")
Options.objects.create(websites=website, groups=checkbox, title="Op3")
Options.objects.create(websites=website, groups=checkbox, title="Readonly", maximum=1, minimum=1)

Options.objects.create(websites=website, groups=numbers, title="Op1", maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Op2", maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Op3", maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Readonly", maximum=5, minimum=5)

radio = Groups.objects.create(websites=website, products=product2, title="radio", maximum=1, minimum=1,
                              price_type='1')
checkbox = Groups.objects.create(websites=website, products=product2, title="checkbox", maximum=1, minimum=0,
                                 price_type='1')
numbers = Groups.objects.create(websites=website, products=product2, title="numbers", maximum=10, minimum=0,
                                price_type='1')

Options.objects.create(websites=website, groups=radio, title="Op1", price=200)
Options.objects.create(websites=website, groups=radio, title="Op2", price=200)
Options.objects.create(websites=website, groups=radio, title="Op3", price=200)
Options.objects.create(websites=website, groups=radio, title="Readonly", price=200, maximum=1, minimum=1)

Options.objects.create(websites=website, groups=checkbox, title="Op1", price=200)
Options.objects.create(websites=website, groups=checkbox, title="Op2", price=200)
Options.objects.create(websites=website, groups=checkbox, title="Op3", price=200)
Options.objects.create(websites=website, groups=checkbox, title="Readonly", price=200, maximum=1, minimum=1)

Options.objects.create(websites=website, groups=numbers, title="Op1", price=200, maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Op2", price=200, maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Op3", price=200, maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Readonly", price=200, maximum=5, minimum=5)

radio = Groups.objects.create(websites=website, products=product3, title="radio", maximum=1, minimum=1,
                              price_type='1')
checkbox = Groups.objects.create(websites=website, products=product3, title="checkbox", maximum=1, minimum=0,
                                 price_type='1')
numbers = Groups.objects.create(websites=website, products=product3, title="numbers", maximum=10, minimum=0,
                                price_type='1')

Options.objects.create(websites=website, groups=radio, title="Op1", price=200)
Options.objects.create(websites=website, groups=radio, title="Op2", price=200)
Options.objects.create(websites=website, groups=radio, title="Op3", price=200)
Options.objects.create(websites=website, groups=radio, title="Readonly", price=200, maximum=1, minimum=1)

Options.objects.create(websites=website, groups=checkbox, title="Op1", price=200)
Options.objects.create(websites=website, groups=checkbox, title="Op2", price=200)
Options.objects.create(websites=website, groups=checkbox, title="Op3", price=200)
Options.objects.create(websites=website, groups=checkbox, title="Readonly", price=200, maximum=1, minimum=1)

Options.objects.create(websites=website, groups=numbers, title="Op1", price=200, maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Op2", price=200, maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Op3", price=200, maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Readonly", price=200, maximum=5, minimum=5)

radio = Groups.objects.create(websites=website, products=product3, title="radio", maximum=1, minimum=1,
                              price_type='2')
checkbox = Groups.objects.create(websites=website, products=product3, title="checkbox", maximum=1, minimum=0,
                                 price_type='2')
numbers = Groups.objects.create(websites=website, products=product3, title="numbers", maximum=10, minimum=0,
                                price_type='2')

Options.objects.create(websites=website, groups=radio, title="Op1", price=200)
Options.objects.create(websites=website, groups=radio, title="Op2", price=200)
Options.objects.create(websites=website, groups=radio, title="Op3", price=200)
Options.objects.create(websites=website, groups=radio, title="Readonly", price=200, maximum=1, minimum=1)

Options.objects.create(websites=website, groups=checkbox, title="Op1", price=200)
Options.objects.create(websites=website, groups=checkbox, title="Op2", price=200)
Options.objects.create(websites=website, groups=checkbox, title="Op3", price=200)
Options.objects.create(websites=website, groups=checkbox, title="Readonly", price=200, maximum=1, minimum=1)

Options.objects.create(websites=website, groups=numbers, title="Op1", price=200, maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Op2", price=200, maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Op3", price=200, maximum=5, minimum=0)
Options.objects.create(websites=website, groups=numbers, title="Readonly", price=200, maximum=5, minimum=5)
