# Асинхронный парсер Python PEP для командной строки
Собирает сводную информацию о PEP в два файла в папке /results

## Как развернуть  

Создать окружение  
```  
python -m venv venv  
```  

Активировать окружение, обновить pip и установить зависимости  
```  
source venv/Scripts/activate  
python -m pip install --upgrade pip  
pip install -r requirements.txt  
```  

Запуститe и посмотрите собранную информацию в /results  
```  
scrapy crawl pep  
```  

По окончании использования деактивировать окружение  
```  
deactivate  
```  

## Стек технологий  
Python, Scrapy  

[Мишустин Василий](https://github.com/vvvas), v@vvvas.ru  
