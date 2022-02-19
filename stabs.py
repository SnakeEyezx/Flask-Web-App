from transliterate import slugify

model = 'Optimum'
brand = 'Энерготех'
voltage_input_type = 'Однофазный'
power = '5000'

product_link = slugify(' '.join(str(item) for item in [model, brand, voltage_input_type, power]))
print(product_link)


