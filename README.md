# Система мониторинга микроклимата
![https://img.shields.io/badge/made%20by-zhichi-brightgreen](https://img.shields.io/badge/made%20by-zhichi-brightgreen)
![https://img.shields.io/pypi/pyversions/Django](https://img.shields.io/pypi/pyversions/Django)
![https://img.shields.io/badge/django%20version-4.0-blue](https://img.shields.io/badge/django%20version-4.0-blue)

Система мониторинга микроклимата предназначена для
отслеживания и хранения параметров микроклимата помещений. В реальном
времени можно контролировать температурные зоны, уровень влажность. Все
данные сохраняются и доступны для просмотра в виде графиков и таблиц.<br>
Данные в систему поступают при помощи API.  
## Скриншоты
![Alt-текст](https://zhichi57.github.io/microclimate_monitoring_system_1.png "")
![Alt-текст](https://zhichi57.github.io/microclimate_monitoring_system_2.png "")
![Alt-текст](https://zhichi57.github.io/microclimate_monitoring_system_3.png "")
![Alt-текст](https://zhichi57.github.io/microclimate_monitoring_system_4.png "")
## Описание API  

Данные передаются по адресу `api/send` в формате `POST`

| Ключ       | Тип   | Описание                                              
| ---------- | ------ | ---------------------------------- 
| `key` | string | Ключ API
| `temp` | float | Значение температуры                          
| `humidity` | float | Значение влажности                          

## Запуск системы с помощью Docker
Для запуска системы с помощью Docker необходимо выполнить команду  
`docker run -p 8000:8000 -t zhichi/microclimate-monitoring-system`

