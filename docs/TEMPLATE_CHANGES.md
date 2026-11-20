# Vorlagen und verbleibende Änderungen

Diese Zuordnung umfasst alle Quelldateien und Paketdateien unter `src/` (ohne Cache-Dateien). Originale stehen unverändert in `templates/`. Die beiden Herkunftszeilen in Python-Dateien sind reine Kommentare. Sie verweisen auf dieses Dokument; der Originalcode darunter behält seine Struktur.

Verglichen wird mit den lokalen Kursvorlagen. `templates/SHA256.json` enthält deren Prüfsummen. Die Vorlagen stimmen nach Normalisierung der Zeilenenden auch mit `../ROS_course/Templates/` überein. Die vorhandene Verschiebung von `reference/templates/` nach `templates/` wurde in diesem Durchgang nicht verändert.

## In diesem Durchgang reduziert

- Unnötige Änderungen an Originalkommentaren in Publisher/Subscriber zurückgenommen.
- Die doppelte Control-Type-Prüfung im TODO von Vorlage 8 auf die einfache Feldübernahme reduziert.
- Keine neuen Regler-, Validierungs-, Kalibrierungs- oder Timeout-Funktionen ergänzt.
- Vorhandene Zusatzdateien nicht umgebaut oder gelöscht; ihre Herkunft und tatsächliche Verwendung sind unten einzeln ausgewiesen.

## Direkte Zuordnung

| Datei | Kursvorlage |
| --- | --- |
| [src/first_package/first_package/simple_publisher.py](../src/first_package/first_package/simple_publisher.py) | [1_simple_publisher.py](../templates/1_simple_publisher.py) |
| [src/first_package/first_package/simple_subscriber.py](../src/first_package/first_package/simple_subscriber.py) | [2_simple_subscriber.py](../templates/2_simple_subscriber.py) |
| [src/first_package/first_package/simple_service.py](../src/first_package/first_package/simple_service.py) | [3_simple_service.py](../templates/3_simple_service.py) |
| [src/first_package/first_package/simple_service_parameter.py](../src/first_package/first_package/simple_service_parameter.py) | [4_simple_service_parameter.py](../templates/4_simple_service_parameter.py) |
| [src/stm_station/stm_station/serial_publisher_node.py](../src/stm_station/stm_station/serial_publisher_node.py) | [6_stm_serial_node_pub.py](../templates/6_stm_serial_node_pub.py) |
| [src/stm_station/stm_station/serial_pubsub_node.py](../src/stm_station/stm_station/serial_pubsub_node.py) | [7_stm_serial_node_pub_sub.py](../templates/7_stm_serial_node_pub_sub.py) |
| [src/stm_station/stm_station/serial_node.py](../src/stm_station/stm_station/serial_node.py) | [7_stm_serial_node_pub_sub.py](../templates/7_stm_serial_node_pub_sub.py) |
| [src/stm_station/stm_station/control_master_slave.py](../src/stm_station/stm_station/control_master_slave.py) | [8_stm_control_node_master_slave.py](../templates/8_stm_control_node_master_slave.py) |
| [src/stm_station/stm_station/control_position.py](../src/stm_station/stm_station/control_position.py) | [9_stm_control_node_master_slave_poscontrol.py](../templates/9_stm_control_node_master_slave_poscontrol.py) |
| [src/stm_station/stm_station/control_node.py](../src/stm_station/stm_station/control_node.py) | [10_stm_control_node_master_slave_impedance_control.py](../templates/10_stm_control_node_master_slave_impedance_control.py) |
| [src/stm_station/stm_station/visualization_node.py](../src/stm_station/stm_station/visualization_node.py) | [11_stm_visualization.py](../templates/11_stm_visualization.py) |
| [src/stm_station/stm_station/turtlebot_control.py](../src/stm_station/stm_station/turtlebot_control.py) | [12_stm_turtlebot_control.py](../templates/12_stm_turtlebot_control.py) |
| [src/stm_station/stm_station/bug0_node.py](../src/stm_station/stm_station/bug0_node.py) | [13_bug0_lidar_stm.py](../templates/13_bug0_lidar_stm.py) |
| [src/stm_station/launch/stm_station_launch.py](../src/stm_station/launch/stm_station_launch.py) | [stm_station_launch.py](../templates/stm_station_launch.py) |
| [src/stm_station/launch/stm_station_launch_all.py](../src/stm_station/launch/stm_station_launch_all.py) | [stm_station_launch_all.py](../templates/stm_station_launch_all.py) |
| [src/stm_station/launch/stm_serial_control_launch.py](../src/stm_station/launch/stm_serial_control_launch.py) | [stm_station_launch.py](../templates/stm_station_launch.py) |
| [src/stm_station/launch/stm_visualization_launch.py](../src/stm_station/launch/stm_visualization_launch.py) | [stm_station_launch_all.py](../templates/stm_station_launch_all.py) |
| [src/stm_station/config/serial_params.yaml](../src/stm_station/config/serial_params.yaml) | [serial_params.yaml](../templates/serial_params.yaml) |

## Änderungen pro Vorlagendatei

Die vollständigen zeilenweisen Unterschiede stehen in [TEMPLATE_DIFF.patch](TEMPLATE_DIFF.patch). Dort sind auch die Herkunftskommentare sichtbar.

### `src/first_package/first_package/simple_publisher.py`

Vorlage: [`1_simple_publisher.py`](../templates/1_simple_publisher.py).

TODOs / Anpassung: Nur die drei vorgegebenen NICKNAME-Platzhalter im Code auf Gruppe 7 gesetzt; Originalkommentare wiederhergestellt.

Notwendige Abweichungen / Grenzen: Keine.

### `src/first_package/first_package/simple_subscriber.py`

Vorlage: [`2_simple_subscriber.py`](../templates/2_simple_subscriber.py).

TODOs / Anpassung: Nur die zwei vorgegebenen NICKNAME-Platzhalter im Code auf Gruppe 7 gesetzt; Originalkommentare wiederhergestellt.

Notwendige Abweichungen / Grenzen: Keine.

### `src/first_package/first_package/simple_service.py`

Vorlage: [`3_simple_service.py`](../templates/3_simple_service.py).

TODOs / Anpassung: Interface-Import, Servicetyp und request.a/request.b ergänzt.

Notwendige Abweichungen / Grenzen: Keine.

### `src/first_package/first_package/simple_service_parameter.py`

Vorlage: [`4_simple_service_parameter.py`](../templates/4_simple_service_parameter.py).

TODOs / Anpassung: Interface-Import, Servicetyp und extra_term = param.value ergänzt.

Notwendige Abweichungen / Grenzen: Fehlenden Import von SetParametersResult ergänzt.

### `src/stm_station/stm_station/serial_publisher_node.py`

Vorlage: [`6_stm_serial_node_pub.py`](../templates/6_stm_serial_node_pub.py).

TODOs / Anpassung: Port-Platzhalter, Float32MultiArray-Publisher, acht Empfangswerte, Nachrichteninhalt und Publish-Aufruf ergänzt.

Notwendige Abweichungen / Grenzen: Die fehlplatzierte Anweisung control_data += ... im Empfangspfad entfernt: Hier gibt es keinen ausgehenden Befehl. Der Originalkommentar bleibt erhalten.

### `src/stm_station/stm_station/serial_pubsub_node.py`

Vorlage: [`7_stm_serial_node_pub_sub.py`](../templates/7_stm_serial_node_pub_sub.py).

TODOs / Anpassung: Wie Vorlage 6; zusätzlich Subscriber, vier Befehlsfelder und serielles Schreiben ergänzt.

Notwendige Abweichungen / Grenzen: Die fehlplatzierte Anweisung control_data += ... im Empfangspfad entfernt. Der Zeilenabschluss wird beim ausgehenden control_data ergänzt.

### `src/stm_station/stm_station/serial_node.py`

Vorlage: [`7_stm_serial_node_pub_sub.py`](../templates/7_stm_serial_node_pub_sub.py).

TODOs / Anpassung: D1.3: Dieselben TODOs wie Vorlage 7, mit STMState/STMControl statt Standard-Array. Acht benannte Zustandsfelder und Zeitstempel gesetzt.

Notwendige Abweichungen / Grenzen: D1.3 erfordert den Austausch der Nachrichtentypen. Für D3 werden serial_port und baud_rate im vorhandenen Konfigurationsblock als Parameter gelesen. Der Zeilenabschluss steht beim Senden statt im Empfangspfad.

### `src/stm_station/stm_station/control_master_slave.py`

Vorlage: [`8_stm_control_node_master_slave.py`](../templates/8_stm_control_node_master_slave.py).

TODOs / Anpassung: Imports, Gruppenparameter, Topics, Subscriber, Publisher, Service, Timer, Positionsübernahme, Servicefelder und Kontrollnachricht ergänzt; dynamische Gruppenwechsel im vorhandenen Callback ausgefüllt.

Notwendige Abweichungen / Grenzen: param.value übernimmt beim Gruppenwechsel den neuen Parameterwert. Eine unnötige zweite Prüfung von request.control_type wurde entfernt; die vorhandene if-Prüfung genügt.

### `src/stm_station/stm_station/control_position.py`

Vorlage: [`9_stm_control_node_master_slave_poscontrol.py`](../templates/9_stm_control_node_master_slave_poscontrol.py).

TODOs / Anpassung: Wie Vorlage 8; zusätzlich Slave-Zustand, Positionsfehler, P-Regelung, Befehlsfelder und Publish-Aufruf ergänzt. Die vorgegebene PWM-Begrenzung bleibt bei 250.

Notwendige Abweichungen / Grenzen: Den falschen Logzugriff self.stm_control_topic zu self.slave_control_topic korrigiert. Im vorhandenen Gruppenwechsel-TODO wird auch der Slave-Zustandssubscriber erneuert, damit Regelung und Befehl dieselbe Gruppe verwenden.

### `src/stm_station/stm_station/control_node.py`

Vorlage: [`10_stm_control_node_master_slave_impedance_control.py`](../templates/10_stm_control_node_master_slave_impedance_control.py).

TODOs / Anpassung: Wie Vorlage 9; zusätzlich Geschwindigkeiten in den Zustands-TODOs gespeichert und PD-Regelung mit Positions- und Geschwindigkeitsfehler ergänzt.

Notwendige Abweichungen / Grenzen: Falschen Logzugriff korrigiert und Slave-Zustand beim Gruppenwechsel aktualisiert wie bei Vorlage 9. Zwei Geschwindigkeitswerte mit 0 initialisiert. request.kd liest das bereits bestehende Servicefeld für den in der Vorlage kv genannten Faktor; lokale kv-Namen bleiben erhalten.

### `src/stm_station/stm_station/visualization_node.py`

Vorlage: [`11_stm_visualization.py`](../templates/11_stm_visualization.py).

TODOs / Anpassung: Gruppenparameter (Standard 7 für Gruppe 7), Topic/Subscriber, Beschleunigungsvektor, Encoderwinkel, Offset, Integration, TF-Aufruf und Transformationsfelder ergänzt.

Notwendige Abweichungen / Grenzen: Die unvollständigen y/z-Integrationszeilen vervollständigt und ihren falschen Index 0 korrigiert. Führenden Slash im TF-Kindframe entfernt. Kein zusätzlicher Path-Publisher, keine Kalibrierungs- oder Hilfsarchitektur ergänzt.

### `src/stm_station/stm_station/turtlebot_control.py`

Vorlage: [`12_stm_turtlebot_control.py`](../templates/12_stm_turtlebot_control.py).

TODOs / Anpassung: Twist importiert; Topic, Subscriber/Publisher, Twist-Nachricht, Geschwindigkeitsumrechnung, Gyroübernahme und Log-Platzhalter ergänzt.

Notwendige Abweichungen / Grenzen: Die Vorlage nennt keinen Radradius: 0,033 m ist weiterhin eine ausdrücklich offene Annahme aus der vorherigen TODO-Lösung. Vor Einsatz an den tatsächlichen Roboter anpassen; die lokale Kursvorlage ist dafür kein Zahlenbeleg.

### `src/stm_station/stm_station/bug0_node.py`

Vorlage: [`13_bug0_lidar_stm.py`](../templates/13_bug0_lidar_stm.py).

TODOs / Anpassung: Nur die TODOs für Subscriber/Publisher, 10-Hz-Timer, Drittel-Aufteilung, Abstände, feste Fahr-/Drehbefehle, Publish-Aufrufe und Log ausgefüllt.

Notwendige Abweichungen / Grenzen: Keine. Konstanten, Hilfsmethode, Klassen und Ablauf bleiben wie in der Vorlage.

### `src/stm_station/launch/stm_station_launch.py`

Vorlage: [`stm_station_launch.py`](../templates/stm_station_launch.py).

TODOs / Anpassung: Ausführbarer Inhalt unverändert; nur der zweizeilige Herkunftshinweis ergänzt.

Notwendige Abweichungen / Grenzen: Keine.

### `src/stm_station/launch/stm_station_launch_all.py`

Vorlage: [`stm_station_launch_all.py`](../templates/stm_station_launch_all.py).

TODOs / Anpassung: Ausführbarer Inhalt unverändert; nur der zweizeilige Herkunftshinweis ergänzt.

Notwendige Abweichungen / Grenzen: Keine.

### `src/stm_station/launch/stm_serial_control_launch.py`

Vorlage: [`stm_station_launch.py`](../templates/stm_station_launch.py).

TODOs / Anpassung: Ausführbarer Inhalt unverändert; nur der zweizeilige Herkunftshinweis ergänzt.

Notwendige Abweichungen / Grenzen: Der vorhandene alternative Dateiname bleibt bei den beiden Alias-Dateien erhalten.

### `src/stm_station/launch/stm_visualization_launch.py`

Vorlage: [`stm_station_launch_all.py`](../templates/stm_station_launch_all.py).

TODOs / Anpassung: Ausführbarer Inhalt unverändert; nur der zweizeilige Herkunftshinweis ergänzt.

Notwendige Abweichungen / Grenzen: Der vorhandene alternative Dateiname bleibt bei den beiden Alias-Dateien erhalten.

### `src/stm_station/config/serial_params.yaml`

Vorlage: [`serial_params.yaml`](../templates/serial_params.yaml).

TODOs / Anpassung: Nur group_id und master_group_id von 1 auf 7 gesetzt.

Notwendige Abweichungen / Grenzen: Keine; beide Werte müssen zur eigenen Gruppe passen.

## Weitere Dateien ohne direkte Vorlage

| Datei | Herkunft / Verwendung / Änderungen in diesem Durchgang |
| --- | --- |
| [src/first_interfaces/CMakeLists.txt](../src/first_interfaces/CMakeLists.txt) | ROS-Paket-/Buildgerüst, keine separate Kursvorlage in templates/. Unverändert in diesem Durchgang. |
| [src/first_interfaces/msg/ExampleMessage.msg](../src/first_interfaces/msg/ExampleMessage.msg) | Eigene ROS-Schnittstellendefinition aus der Kursaufgabe; keine separate Datei in templates/. Unverändert. |
| [src/first_interfaces/package.xml](../src/first_interfaces/package.xml) | ROS-Paket-/Buildgerüst, keine separate Kursvorlage in templates/. Unverändert in diesem Durchgang. |
| [src/first_interfaces/srv/ExampleService.srv](../src/first_interfaces/srv/ExampleService.srv) | Eigene ROS-Schnittstellendefinition aus der Kursaufgabe; keine separate Datei in templates/. Unverändert. |
| [src/first_package/first_package/__init__.py](../src/first_package/first_package/__init__.py) | Python-Paketdatei, keine Kursvorlage. Unverändert. |
| [src/first_package/first_package/simple_pubsub_node.py](../src/first_package/first_package/simple_pubsub_node.py) | Vorlagen 1 + 2, kombiniert. Vorhandener Zusatzknoten für ExampleMessage auf topic_7/topic_7_out; keine direkte Vorlagenkopie. In diesem Durchgang nur diesen Herkunftshinweis ergänzt. |
| [src/first_package/package.xml](../src/first_package/package.xml) | ROS-Paket-/Buildgerüst, keine separate Kursvorlage in templates/. Unverändert in diesem Durchgang. |
| [src/first_package/resource/first_package](../src/first_package/resource/first_package) | ROS-Paket-/Buildgerüst, keine separate Kursvorlage in templates/. Unverändert in diesem Durchgang. |
| [src/first_package/setup.cfg](../src/first_package/setup.cfg) | ROS-Paket-/Buildgerüst, keine separate Kursvorlage in templates/. Unverändert in diesem Durchgang. |
| [src/first_package/setup.py](../src/first_package/setup.py) | ROS-Paket-/Buildgerüst, keine separate Kursvorlage in templates/. Unverändert in diesem Durchgang. |
| [src/first_package/test/test_copyright.py](../src/first_package/test/test_copyright.py) | Vorhandener Test-/Gerüstcode, keine nummerierte Kursvorlage. Unverändert; Hilfsmodultests prüfen die frühere Hilfslogik, nicht die aktuellen Node-Callbacks. |
| [src/first_package/test/test_flake8.py](../src/first_package/test/test_flake8.py) | Vorhandener Test-/Gerüstcode, keine nummerierte Kursvorlage. Unverändert; Hilfsmodultests prüfen die frühere Hilfslogik, nicht die aktuellen Node-Callbacks. |
| [src/first_package/test/test_pep257.py](../src/first_package/test/test_pep257.py) | Vorhandener Test-/Gerüstcode, keine nummerierte Kursvorlage. Unverändert; Hilfsmodultests prüfen die frühere Hilfslogik, nicht die aktuellen Node-Callbacks. |
| [src/stm_interfaces/CMakeLists.txt](../src/stm_interfaces/CMakeLists.txt) | ROS-Paket-/Buildgerüst, keine separate Kursvorlage in templates/. Unverändert in diesem Durchgang. |
| [src/stm_interfaces/msg/STMControl.msg](../src/stm_interfaces/msg/STMControl.msg) | Eigene ROS-Schnittstellendefinition aus der Kursaufgabe; keine separate Datei in templates/. Unverändert. |
| [src/stm_interfaces/msg/STMState.msg](../src/stm_interfaces/msg/STMState.msg) | Eigene ROS-Schnittstellendefinition aus der Kursaufgabe; keine separate Datei in templates/. Unverändert. |
| [src/stm_interfaces/package.xml](../src/stm_interfaces/package.xml) | ROS-Paket-/Buildgerüst, keine separate Kursvorlage in templates/. Unverändert in diesem Durchgang. |
| [src/stm_interfaces/srv/STMSetControlType.srv](../src/stm_interfaces/srv/STMSetControlType.srv) | Eigene ROS-Schnittstellendefinition aus der Kursaufgabe; keine separate Datei in templates/. Unverändert. STMSetControlType verwendet weiterhin kd. |
| [src/stm_station/config/bug0_params.yaml](../src/stm_station/config/bug0_params.yaml) | Konfiguration der früheren Umsetzung; vom aktuellen Bug0-Node nicht gelesen. Unverändert belassen. |
| [src/stm_station/launch/stm_bug0_launch.py](../src/stm_station/launch/stm_bug0_launch.py) | Launch-Pattern + Vorlage 13. Vorhandener Ein-Knoten-Start für bug0_lidar_stm_node; keine eigene Kursvorlage. Nur Herkunftshinweis ergänzt. |
| [src/stm_station/launch/stm_serial_node_launch.py](../src/stm_station/launch/stm_serial_node_launch.py) | Launch-Pattern aus stm_station_launch.py. Vorhandener Ein-Knoten-Start für stm_serial_node in group_7; keine eigene Kursvorlage. Nur Herkunftshinweis ergänzt. |
| [src/stm_station/package.xml](../src/stm_station/package.xml) | ROS-Paket-/Buildgerüst, keine separate Kursvorlage in templates/. Unverändert in diesem Durchgang. |
| [src/stm_station/resource/stm_station](../src/stm_station/resource/stm_station) | ROS-Paket-/Buildgerüst, keine separate Kursvorlage in templates/. Unverändert in diesem Durchgang. |
| [src/stm_station/rviz/stm_config.rviz](../src/stm_station/rviz/stm_config.rviz) | Eigene RViz-Konfiguration; keine Kursvorlage. Unverändert. Der enthaltene Path-Display bekommt von Vorlage 11 keine Daten. |
| [src/stm_station/setup.cfg](../src/stm_station/setup.cfg) | ROS-Paket-/Buildgerüst, keine separate Kursvorlage in templates/. Unverändert in diesem Durchgang. |
| [src/stm_station/setup.py](../src/stm_station/setup.py) | ROS-Paketregistrierung, keine Kursvorlage. Bereits auf Vorlagen-Nodes und zehn Einstiegspunkte angepasst; in diesem Durchgang unverändert. |
| [src/stm_station/stm_station/__init__.py](../src/stm_station/stm_station/__init__.py) | Python-Paketdatei, keine Kursvorlage. Unverändert. |
| [src/stm_station/stm_station/bug0.py](../src/stm_station/stm_station/bug0.py) | Zusatzcode der früheren Umsetzung, keine direkte Vorlage. Frühere ausgelagerte Bug0-Logik; nicht vom aktuellen bug0_node importiert. Unverändert belassen. |
| [src/stm_station/stm_station/launch_settings.py](../src/stm_station/stm_station/launch_settings.py) | Zusatzcode der früheren Umsetzung, keine direkte Vorlage. Frühere Launch-Validierung; nicht von den aktuellen Launch-Dateien importiert. Unverändert belassen. |
| [src/stm_station/stm_station/motion.py](../src/stm_station/stm_station/motion.py) | Zusatzcode der früheren Umsetzung, keine direkte Vorlage. Früherer MotionEstimate mit zusätzlicher Kalibrierung; nicht vom aktuellen visualization_node importiert. Unverändert belassen. |
| [src/stm_station/stm_station/protocol.py](../src/stm_station/stm_station/protocol.py) | Zusatzcode der früheren Umsetzung, keine direkte Vorlage. Frühere Parser-/Regler-Hilfslogik; nicht von den aktuellen Vorlagen-Nodes importiert. Unverändert belassen. |
| [src/stm_station/stm_station/standard_serial_node.py](../src/stm_station/stm_station/standard_serial_node.py) | Zusatzcode der früheren Umsetzung, keine direkte Vorlage. Frühere Stufen-Abstraktion; kein aktueller Einstiegspunkt. Importiert eine nicht mehr vorhandene SerialNode-Klasse und ist daher kein lauffähiger aktueller Node. Unverändert belassen. |
| [src/stm_station/test/test_bug0.py](../src/stm_station/test/test_bug0.py) | Vorhandener Test-/Gerüstcode, keine nummerierte Kursvorlage. Unverändert; Hilfsmodultests prüfen die frühere Hilfslogik, nicht die aktuellen Node-Callbacks. |
| [src/stm_station/test/test_motion.py](../src/stm_station/test/test_motion.py) | Vorhandener Test-/Gerüstcode, keine nummerierte Kursvorlage. Unverändert; Hilfsmodultests prüfen die frühere Hilfslogik, nicht die aktuellen Node-Callbacks. |
| [src/stm_station/test/test_package_assets.py](../src/stm_station/test/test_package_assets.py) | Eigener Pakettest, keine Kursvorlage. Erwartete Launch-Dateien und Einstiegspunktzahl an die bereits vorhandenen Vorlagen-Stufen angepasst. |
| [src/stm_station/test/test_protocol.py](../src/stm_station/test/test_protocol.py) | Vorhandener Test-/Gerüstcode, keine nummerierte Kursvorlage. Unverändert; Hilfsmodultests prüfen die frühere Hilfslogik, nicht die aktuellen Node-Callbacks. |
| [src/stm_station/test/test_ros_launch.py](../src/stm_station/test/test_ros_launch.py) | Eigener ROS-Launchtest, keine Kursvorlage. Alte Zusatzargument-/launch_nodes-Tests durch Aufrufe der vorhandenen generate_launch_description-Funktionen ersetzt. Wird ohne ROS übersprungen. |
| [src/stm_station/test/test_stages_and_launch_settings.py](../src/stm_station/test/test_stages_and_launch_settings.py) | Vorhandener Test-/Gerüstcode, keine nummerierte Kursvorlage. Unverändert; Hilfsmodultests prüfen die frühere Hilfslogik, nicht die aktuellen Node-Callbacks. |

## Vorlage 5

[5_stm_serial_communication_python.py](../templates/5_stm_serial_communication_python.py) ist die vollständige serielle GUI ohne TODOs. Sie bleibt unverändert in `templates/`; es gibt keine separate, umgeschriebene Kopie in `src/`.

## Verifikation und offene Punkte

Syntax, Einstiegspunkte, Vorlagenprüfsummen sowie Klassen-/Methodenstruktur werden separat geprüft. Die Paket- und vorhandenen Hilfsmodultests können lokal laufen. Ein Callback-Smoke-Test prüft die aktuellen TODO-Lösungen ohne ROS und Hardware. Das ersetzt keine ROS-, Gazebo- oder Hardwaretests.

Der angenommene Radradius in Vorlage 12 bleibt vor Roboternutzung zu klären. Vorlage 11 sendet TF, enthält aber keinen ausgefüllten Path-Publisher. Die alten README-Abschnitte zu Zusatzfunktionen sind historische Aufzeichnungen; maßgeblich sind die Vorlagen-Nodes und die neue Zuordnung oben.

### Ergebnis dieses Durchgangs

- `python -m pytest src/stm_station/test -q` mit `src/stm_station` im Python-Suchpfad: **57 bestanden, 1 übersprungen**. Der übersprungene Test benötigt ROS. Das lokal fehlende `setuptools` wurde nur in einem temporären Prüfverzeichnis bereitgestellt.
- Zusätzlicher temporärer Smoke-/Strukturcheck: **140 Assertions bestanden**. Geprüft wurden Originalprüfsummen, jede Quelldatei in der Zuordnung, unveränderte Klassen-/Methodennamen sowie Empfang/Senden, Controller-Modi und Gruppenwechsel, Bug0-Zweige, TF/Integration und Services. Die ROS-Objekte wurden dabei durch lokale Testobjekte ersetzt.
- Python-Syntax aller Quelldateien geprüft. ROS-, Gazebo- und Hardwarebetrieb bleiben ungeprüft.
