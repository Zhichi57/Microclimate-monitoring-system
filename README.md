<h1 align="center">Система мониторинга микроклимата</h1>
<p align="center">
<img src="https://img.shields.io/badge/made%20by-zhichi-brightgreen">
<img src="https://img.shields.io/pypi/pyversions/Django">
<img src="https://img.shields.io/badge/django%20version-4.0-blue">
</p>

Система мониторинга микроклимата предназначена для
отслеживания и хранения параметров микроклимата помещений. В реальном
времени можно контролировать температурные зоны, уровень влажность. Все
данные сохраняются и доступны для просмотра в виде графиков и таблиц.<br>
Данные в систему поступают при помощи API.
---
<h2>Скриншоты</h2>
<img src="https://zhichi57.github.io/microclimate_monitoring_system_1.png">
<img src="https://zhichi57.github.io/microclimate_monitoring_system_2.png">
<img src="https://zhichi57.github.io/microclimate_monitoring_system_3.png">
<img src="https://zhichi57.github.io/microclimate_monitoring_system_4.png">
---
<h2>Описание API</h2>
Данные передаются по адресу `api/send` в формате `POST`

| Ключ       | Тип   | Описание                                              
| ---------- | ------ | ---------------------------------- 
| `key` | string | Ключ API
| `temp` | float | Значение температуры                          
| `humidity` | float | Значение влажности                          