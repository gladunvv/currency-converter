# currency-converter
API currency converter on Python

# Краткое описание
Простое API на Flask которое по запросу отдаёт конвертированную валюту по актуальному курсу, для этого необходимо в качестве аргументов в URL передавать три параметра:          
**input_currency** - конвертируемая валюта               
**output_currency** - валюта в которую будет конвентированна сумма             
**amount** - сумма которую следует конвертировать          
Для полноценной работы необходимо создать *app/.env* и внутри этого файла прописать API_KEY к ресурсу [Fixer API](https://fixer.io/)


## Requirements
* Click==7.0
* Flask==1.1.1
* itsdangerous==1.1.0
* Jinja2==2.10.3
* MarkupSafe==1.1.1
* python-dotenv==0.10.3
* Werkzeug==0.16.0

## Сборка и запуск
```bash
git clone git@github.com:gladunvv/currency-converter.git
python3 -m venv venv
source venv/bin/activate 
pip install requirements.txt
cd app
flask run
```

## Пример:  

### Запрос:
>GET: http://127.0.0.1:5000/currency_converte?input_currency=RUB&output_currency=USD&amount=35000
### Ответ:
```json
{
  "input": {
    "amount": 35000.0, 
    "currency": "RUB"
  }, 
  "output": {
    "USD": 549.71
  }
}
```

## License
This project is licensed under the terms of the MIT license