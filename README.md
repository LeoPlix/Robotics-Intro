# Athens ROS 2 - Team WinningLeos

Group 7, ATHENS 2026, UPM Madrid. We use Ubuntu 24.04 and ROS 2 Jazzy in the course VM.

## Deliverables

Work through the sections below in order. Each has the task, commands by terminal, expected behavior, stop commands and a table for our results. Save screenshots in the matching subtask folder.

| Task | Instructions | Status |
| --- | --- | --- |
| D1 | [STM communication](#d1) | Publisher, subscriber and custom-message stages implemented |
| D2 | [Master/slave control](#d2) | Position and impedance modes implemented |
| D3 | [Launch files](#d3) | Single and combined startup implemented |
| D4 | [RViz visualization](#d4) | TF, trajectory and plots implemented |
| D5 | [Robot navigation](#d5) | Bug0 simulation code implemented; real-robot tests and STM mapping open |

The code still needs testing in ROS, Gazebo and on the course hardware. Record what actually happens in the task test table before marking a task complete.

## Setup

Clone once, or use git pull in an existing checkout:

```bash
git clone https://github.com/Athens-ROS2-Course/Athens-ROS2-Team-WinningLeos.git
cd Athens-ROS2-Team-WinningLeos
```

From the repository root in Ubuntu:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
mkdir -p bags
ls -l /dev/serial/by-id/
```

```bash
colcon build --symlink-install
source install/setup.bash
ros2 run stm_station stm_serial_node_pub
ros2 run stm_station stm_serial_node_pub_sub
ros2 run stm_station stm_serial_node
ros2 run stm_station stm_control_node_master_slave
ros2 run stm_station stm_control_node_master_slave_poscontrol
ros2 run stm_station stm_control_node_master_slave_impedance_control
ros2 launch stm_station stm_station_launch.py
ros2 launch stm_station stm_station_launch_all.py
```

In every new terminal, return to the repository and source both setup files. Use the actual USB device paths, and pass the STM devices through to the VM. Serial access may require membership in dialout and a new login session.

Our group is 7. Group 2 in the D2/D3 examples is only a partner placeholder: replace it with the real partner group. Run one bridge per USB device and one command publisher per station.

## Repository layout

```text
src/
  first_interfaces/   # Introductory message/service exercises
  first_package/      # Introductory ROS nodes
  stm_interfaces/     # STMState, STMControl, STMSetControlType
  stm_station/        # Nodes, launch files, configuration and tests
reference/templates/  # Original course exercises with TODOs
deliverables/
  D1/ ... D5/         # Subtask folders, e.g. D1/D1.1/ for screenshots
```

Configuration files are in src/stm_station/config. Group IDs and ports are launch arguments; the sections below show the exact commands. Original templates are references, not finished solutions.

## Tests

The tests in src/stm_station/test check parsing, control calculations, motion estimation, Bug0 decisions and package assets:

```bash
PYTHONPATH=src/stm_station python3 -m pytest src/stm_station/test -q
```

On the ROS machine, also run:

```bash
colcon test --packages-select stm_station
colcon test-result --verbose
```

These checks do not replace the movement, stop and recording tests in D1-D5.

## Screenshots and submission

Use names such as deliverables/D1/D1.1/graph.png or deliverables/D4/D4.2/position_plot.png. Save actual gains, ports, units and the tested commit alongside the result. Start rosbag recording before the demonstration and stop it cleanly with Ctrl+C.

Keep screenshots and short logs in Git. Upload large bags/videos to the agreed course storage, check that the lecturers can access them, and put links in the matching task section. Record the required course upload or live demonstration separately from the code status.

## Course material

The task sections map the current Athens2026_ROS2.pptx and the older Athens_ROS2_Course.pptx to their slide numbers. Both decks remain in the course Material folder.

The [original ROS_course templates](https://github.com/Robolabo/ROS_course/tree/cf9e122904ebcb55d336aa7e82d0760bc94cbb07) are attributed to their upstream revision. D5 uses the external Galileo simulator; its pinned setup and command interface are documented in [D5](#d5-1-simulation).

## Task instructions

Open a section to see its commands and test table. `deliverables` contains only subtask folders for screenshots and results; empty folders use a .gitkeep file so Git includes them.

<a id="d1"></a>

<details>
<summary>D1 - STM communication</summary>

Use a separate terminal for each running node or recorder. In every terminal, source Jazzy and the workspace as shown in the root README. Record bags before the demonstration and close the recorder with Ctrl+C.

## Message format

D1.1 and D1.2 use Float32MultiArray. The state array contains encoder position, motor velocity, acceleration x/y/z and gyro x/y/z. D1.2 commands contain `[mode, setpoint, kp, pwm]`. D1.3 replaces these arrays with STMState and STMControl.

The serial format stays the same: `{encoder,velocity,ax,ay,az,gx,gy,gz}` for state and `{mode,setpoint,kp,pwm}` for commands, each followed by a newline. Firmware modes are 0 stop, 1 onboard position control and 2 PWM. The bridge caps PWM at +/-250 and sends stop after 0.5 seconds without a new command. Check units, direction and firmware watchdog behavior at the station.

Serial defaults are 115200 baud and 100 Hz polling. Set the port at startup. Build and source the workspace before running any stage. Stop the old stage before switching to the next one.

<a id="d1-1"></a>

## D1.1 - Standard-message publisher

**Prerequisites:** One STM attached and serial permissions configured; previous stages stopped.

Observe encoder/IMU changes while keeping the state stream live. Check that no command subscriber exists.

**Terminal A:** Start only this exercise stage.

```bash
ros2 run stm_station stm_serial_node_pub --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start recording before demonstrating movement.

```bash
ros2 bag record -o bags/d1_1_run01 /group_7/stm_state
```

**Terminal C:** Inspect the interfaces and graph. Close long-running viewers before the next command.

```bash
ros2 topic type /group_7/stm_state
ros2 topic echo /group_7/stm_state --once
ros2 node info /group_7/stm_serial_node
rqt_graph
```

**Expected:** Float32MultiArray contains eight values in encoder, velocity, acceleration xyz, gyro xyz order; no stm_control subscription.

**Stop:** Ctrl+C recorder, then bridge; close graph. Run `ros2 bag info bags/d1_1_run01` after recording.

**Save:** State output, node/topic graph, interface type and bag in `deliverables/D1/` or link the bag from the result table.

<a id="d1-2"></a>

## D1.2 - Standard-message publisher and subscriber

**Prerequisites:** One STM attached and serial permissions configured; previous stages stopped.

Observe encoder/IMU changes while keeping the state stream live. Demonstrate command reception and timeout stop.

**Terminal A:** Start only this exercise stage.

```bash
ros2 run stm_station stm_serial_node_pub_sub --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start recording before demonstrating movement.

```bash
ros2 bag record -o bags/d1_2_run01 /group_7/stm_state /group_7/stm_control
```

**Terminal C:** Inspect the interfaces and graph. Close long-running viewers before the next command.

```bash
ros2 topic type /group_7/stm_state
ros2 topic echo /group_7/stm_state --once
ros2 node info /group_7/stm_serial_node
rqt_graph
```

**Terminal D:** First send stop; Ctrl+C that publisher before the small PWM test. Verify firmware direction/range first.

```bash
ros2 topic pub --rate 10 /group_7/stm_control std_msgs/msg/Float32MultiArray "{data: [0.0, 0.0, 0.0, 0.0]}"
# After Ctrl+C, start the next publisher:
ros2 topic pub --rate 10 /group_7/stm_control std_msgs/msg/Float32MultiArray "{data: [2.0, 0.0, 0.0, 10.0]}"
```

**Expected:** Both topics use Float32MultiArray; valid commands reach the motor while state publication continues.

**Stop:** Ctrl+C any command publisher; for D1.2/1.3 observe motor stop after approximately 0.5 seconds without commands. Ctrl+C recorder, then bridge; close graph. Run `ros2 bag info bags/d1_2_run01` after recording.

**Save:** State output, node/topic graph, interface types and bag; for command stages include a short response/stop video and measured observations. Save results and links in the matching subtask folder under `deliverables/D1/`.

<a id="d1-3"></a>

## D1.3 - Custom STM interfaces

**Prerequisites:** One STM attached and serial permissions configured; previous stages stopped.

Observe encoder/IMU changes while keeping the state stream live. Demonstrate command reception and timeout stop.

**Terminal A:** Start only this exercise stage.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start recording before demonstrating movement.

```bash
ros2 bag record -o bags/d1_3_run01 /group_7/stm_state /group_7/stm_control
```

**Terminal C:** Inspect the interfaces and graph. Close long-running viewers before the next command.

```bash
ros2 interface show stm_interfaces/msg/STMState
ros2 interface show stm_interfaces/msg/STMControl
ros2 topic type /group_7/stm_state
ros2 topic echo /group_7/stm_state --once
ros2 node info /group_7/stm_serial_node
rqt_graph
```

**Terminal D:** First send stop; Ctrl+C that publisher before the small PWM test. Verify firmware direction/range first.

```bash
ros2 topic pub --rate 10 /group_7/stm_control stm_interfaces/msg/STMControl "{control_type: 0}"
# After Ctrl+C, start the next publisher:
ros2 topic pub --rate 10 /group_7/stm_control stm_interfaces/msg/STMControl "{control_type: 2, pwm: 10.0}"
```

**Expected:** State/control types are STMState and STMControl, with named fields and advancing state stamps.

**Stop:** Ctrl+C any command publisher; for D1.2/1.3 observe motor stop after approximately 0.5 seconds without commands. Ctrl+C recorder, then bridge; close graph. Run `ros2 bag info bags/d1_3_run01` after recording.

**Save:** State output, node/topic graph, interface types and bag; for command stages include a short response/stop video and measured observations. Save results and links in the matching subtask folder under `deliverables/D1/`.

## Course slides and templates

Current slides refer to Athens2026_ROS2.pptx; older slides refer to Athens_ROS2_Course.pptx. A star marks an extension task.

| Task | Current slides | Older slides | Original template |
| --- | --- | --- | --- |
| D1.1 | 78 | 84 | [6_stm_serial_node_pub.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/6_stm_serial_node_pub.py) |
| D1.2 | 79 | 85 | [7_stm_serial_node_pub_sub.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/7_stm_serial_node_pub_sub.py) |
| D1.3 | 80-81 | 86-87 | [7_stm_serial_node_pub_sub.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/7_stm_serial_node_pub_sub.py) |

<a id="d1-test-log"></a>

## Test log

ROS/hardware results have not been recorded yet. After each run, fill in the tested commit, actual ports, gains and observations.

| Task | Date / tester / commit | Result | Notes and evidence |
| --- | --- | --- | --- |
| D1.1 | | Not run | |
| D1.2 | | Not run | |
| D1.3 | | Not run | |

<a id="d1-evidence"></a>

## Evidence

Save screenshots and small text files in the matching subtask folder, for example `deliverables/D1/D1.1/graph.png`. Add filenames or links to the test table. Keep large videos and bags in the agreed course storage and link them here.

Submission date / course upload link / demonstration: not recorded.

</details>

<a id="d2"></a>

<details>
<summary>D2 - Master/slave control</summary>

Use a separate terminal for each running node or recorder. In every terminal, source Jazzy and the workspace as shown in the root README. Record bags before the demonstration and close the recorder with Ctrl+C.

## Controller settings

Our station is Group 7. Group 2 below is an example partner; replace its ID and port with the actual second station. Group parameters are startup-only.

Service modes are 0 stop, 1 master position sent to the slave's onboard position controller, and 2 host PWM control. Mode 2 computes `kp * position_error + kd * velocity_error`: use kd=0 for D2.2 and kd>0 for D2.3. The gains below are starting examples to tune on the device.

Standalone commands expose `/stm_setcontrol_type`. With the combined D3 launch, use `/group_7/stm_setcontrol_type` instead. Invalid requests stop and return success=false. Lost feedback stops and disarms the controller after 0.5 seconds; restore the feedback and call the service again to resume.

<a id="d2-1"></a>

## D2.1 - Master/slave onboard position

**Prerequisites:** D1.3 working on two stations, IDs/ports verified, no other controller or manual slave command publisher.

Use separate terminals for both bridges. Gains below are examples to tune on your hardware. The controller starts in stop; arm only after both state streams are present. D2.2 and D2.3 are starred extensions.

**Terminal A:** Start our custom master bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start the partner custom slave bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_2 -p port:=/dev/ttyACM1
```

**Terminal C:** Start one controller with reduced host PWM limit. Onboard position mode uses firmware behavior, not this PWM clamp.

```bash
ros2 run stm_station stm_control_node --ros-args -p master_group_id:=7 -p slave_group_id:=2 -p pwm_limit:=25.0
```

**Terminal D:** Start the recording before enabling control.

```bash
ros2 bag record -o bags/d2_1_run01 /group_7/stm_state /group_2/stm_state /group_2/stm_control
```

**Terminal E:** Check states, then enable this mode and move the master slowly.

```bash
ros2 topic echo /group_7/stm_state --once
ros2 topic echo /group_2/stm_state --once
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 1, kp: 1.0, kd: 0.0}"
ros2 topic echo /group_2/stm_control --once
ros2 node info /stm_control_node
```

**Expected:** Slave setpoint follows master encoder, with control_type=1. Valid service requests return success=true.

**Stop:** In Terminal E run `ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"`. Observe stop. Also test invalid mode 99 (success=false) and interrupted master feedback (stop/disarm; explicit rearm required). Ctrl+C recorder, controller and bridges, in that order.

**Save:** Two state traces, slave command trace, graph and video. Record exact gains/units, firmware, PWM limit and stop/feedback-loss results. For P/PD include plots comparing master and slave. Save results and links in the matching subtask folder under `deliverables/D2/`.

<a id="d2-2"></a>

## D2.2 - Host position P controller

**Prerequisites:** D1.3 working on two stations, IDs/ports verified, no other controller or manual slave command publisher.

Use separate terminals for both bridges. Gains below are examples to tune on your hardware. The controller starts in stop; arm only after both state streams are present. D2.2 and D2.3 are starred extensions.

**Terminal A:** Start our custom master bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start the partner custom slave bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_2 -p port:=/dev/ttyACM1
```

**Terminal C:** Start one controller with reduced host PWM limit. Onboard position mode uses firmware behavior, not this PWM clamp.

```bash
ros2 run stm_station stm_control_node --ros-args -p master_group_id:=7 -p slave_group_id:=2 -p pwm_limit:=25.0
```

**Terminal D:** Start the recording before enabling control.

```bash
ros2 bag record -o bags/d2_2_run01 /group_7/stm_state /group_2/stm_state /group_2/stm_control
```

**Terminal E:** Check states, then enable this mode and move the master slowly.

```bash
ros2 topic echo /group_7/stm_state --once
ros2 topic echo /group_2/stm_state --once
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 2, kp: 1.0, kd: 0.0}"
ros2 topic echo /group_2/stm_control --once
ros2 node info /stm_control_node
```

**Expected:** Slave receives mode 2 PWM: kp*position_error, clamped to +/-25. Compare physical tracking against recorded master/slave traces. Valid service requests return success=true.

**Stop:** In Terminal E run `ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"`. Observe stop. Also test invalid mode 99 (success=false) and interrupted master feedback (stop/disarm; explicit rearm required). Ctrl+C recorder, controller and bridges, in that order.

**Save:** Two state traces, slave command trace, graph and video. Record exact gains/units, firmware, PWM limit and stop/feedback-loss results. For P/PD include plots comparing master and slave. Save results and links in the matching subtask folder under `deliverables/D2/`.

<a id="d2-3"></a>

## D2.3 - Host impedance PD controller

**Prerequisites:** D1.3 working on two stations, IDs/ports verified, no other controller or manual slave command publisher.

Use separate terminals for both bridges. Gains below are examples to tune on your hardware. The controller starts in stop; arm only after both state streams are present. D2.2 and D2.3 are starred extensions.

**Terminal A:** Start our custom master bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_7 -p port:=/dev/ttyACM0
```

**Terminal B:** Start the partner custom slave bridge.

```bash
ros2 run stm_station stm_serial_node --ros-args -r __ns:=/group_2 -p port:=/dev/ttyACM1
```

**Terminal C:** Start one controller with reduced host PWM limit. Onboard position mode uses firmware behavior, not this PWM clamp.

```bash
ros2 run stm_station stm_control_node --ros-args -p master_group_id:=7 -p slave_group_id:=2 -p pwm_limit:=25.0
```

**Terminal D:** Start the recording before enabling control.

```bash
ros2 bag record -o bags/d2_3_run01 /group_7/stm_state /group_2/stm_state /group_2/stm_control
```

**Terminal E:** Check states, then enable this mode and move the master slowly.

```bash
ros2 topic echo /group_7/stm_state --once
ros2 topic echo /group_2/stm_state --once
ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 2, kp: 1.0, kd: 0.1}"
ros2 topic echo /group_2/stm_control --once
ros2 node info /stm_control_node
```

**Expected:** Slave receives mode 2 PWM: kp*position_error + kd*velocity_error, clamped to +/-25. Compare physical tracking against recorded master/slave traces. Valid service requests return success=true.

**Stop:** In Terminal E run `ros2 service call /stm_setcontrol_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"`. Observe stop. Also test invalid mode 99 (success=false) and interrupted master feedback (stop/disarm; explicit rearm required). Ctrl+C recorder, controller and bridges, in that order.

**Save:** Two state traces, slave command trace, graph and video. Record exact gains/units, firmware, PWM limit and stop/feedback-loss results. For P/PD include plots comparing master and slave. Save results and links in the matching subtask folder under `deliverables/D2/`.

## Course slides and templates

Current slides refer to Athens2026_ROS2.pptx; older slides refer to Athens_ROS2_Course.pptx. A star marks an extension task.

| Task | Current slides | Older slides | Original template |
| --- | --- | --- | --- |
| D2.1 | 92-93 | 106-107, 109 | [8_stm_control_node_master_slave.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/8_stm_control_node_master_slave.py) |
| D2.2* | 95 | 109 | [9_stm_control_node_master_slave_poscontrol.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/9_stm_control_node_master_slave_poscontrol.py) |
| D2.3* | 96-97 | 110-111 | [10_stm_control_node_master_slave_impedance_control.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/10_stm_control_node_master_slave_impedance_control.py) |

<a id="d2-test-log"></a>

## Test log

ROS/hardware results have not been recorded yet. After each run, fill in the tested commit, actual ports, gains and observations.

| Task | Date / tester / commit | Result | Notes and evidence |
| --- | --- | --- | --- |
| D2.1 | | Not run | |
| D2.2 | | Not run | |
| D2.3 | | Not run | |

<a id="d2-evidence"></a>

## Evidence

Save screenshots and small text files in the matching subtask folder, for example `deliverables/D2/D2.1/graph.png`. Add filenames or links to the test table. Keep large videos and bags in the agreed course storage and link them here.

Submission date / course upload link / demonstration: not recorded.

</details>

<a id="d3"></a>

<details>
<summary>D3 - Launch files</summary>

Use a separate terminal for each running node or recorder. In every terminal, source Jazzy and the workspace as shown in the root README. Record bags before the demonstration and close the recorder with Ctrl+C.

## Configuration

D3 follows the original course template: the launch reads group_id from the installed config/serial_params.yaml, builds the namespace and passes that YAML to the nodes. Edit that YAML in src/stm_station/config before building. Our group is 7; replace slave_group_id=2 with the actual partner group. Serial settings use the template names serial_port and baud_rate.

stm_station_launch.py is unchanged from templates/stm_station_launch.py. stm_serial_control_launch.py retains the same template as a compatibility filename. The single-node version only omits the controller. No additional launch arguments or automatic second bridge are used.

<a id="d3-1-0"></a>

## D3.1.0 - Single-station launch

After building and sourcing the workspace, start the serial bridge:

```bash
ros2 launch stm_station stm_serial_node_launch.py
```

In another sourced terminal:

```bash
ros2 node info /group_7/stm_serial_node
ros2 param get /group_7/stm_serial_node baud_rate
ros2 topic echo /group_7/stm_state --once
```

Expected: one bridge, baud_rate=115200 and incoming state. Save node info, parameters and state output in deliverables/D3/D3.1.0/. Stop with Ctrl+C before the combined launch.

<a id="d3-1-1"></a>

## D3.1.1 - Launch/config installation

```bash
colcon build --symlink-install --packages-up-to stm_station
source install/setup.bash
ls "$(ros2 pkg prefix --share stm_station)/launch"
ls "$(ros2 pkg prefix --share stm_station)/config"
ls "$(ros2 pkg prefix --share stm_station)/rviz"
(cd /tmp && ros2 launch stm_station stm_station_launch.py --show-args)
```

Expected: launch files, serial_params.yaml and stm_config.rviz are installed. Argument inspection succeeds outside the workspace; the course template declares no launch arguments. Save build and listing output in deliverables/D3/D3.1.1/.

<a id="d3-2"></a>

## D3.2 - Combined launch

Stop the single bridge first. The partner starts its own bridge on the same ROS network using its own group ID and device configuration. This launch starts our bridge and the master/slave controller:

```bash
ros2 launch stm_station stm_station_launch.py
```

In another sourced terminal:

```bash
ros2 node list
ros2 param get /group_7/stm_control_node_master_slave master_group_id
ros2 param get /group_7/stm_control_node_master_slave slave_group_id
ros2 service call /group_7/set_control_type stm_interfaces/srv/STMSetControlType "{control_type: 0, kp: 0.0, kd: 0.0}"
rqt_graph
```

Expected: our bridge and controller, partner bridge visible on the ROS network, configured group IDs and successful stop service. Save graph, parameters and service output in deliverables/D3/D3.2/. Stop with Ctrl+C and verify that the launched processes exit.

## Course slides and templates

Current slides refer to Athens2026_ROS2.pptx; older slides refer to Athens_ROS2_Course.pptx. A star marks an extension task.

| Task | Current slides | Older slides | Original template |
| --- | --- | --- | --- |
| D3.1.0 | 102 | 115 | [stm_station_launch.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/stm_station_launch.py) |
| D3.1.1 | 102 | 116 | [stm_station_launch.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/stm_station_launch.py) |
| D3.2 | 102 | 117 | [stm_station_launch.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/stm_station_launch.py) |

The current slides call the combined launch D3.1. The older slides split single launch, packaging and combined launch into the three steps above.

<a id="d3-test-log"></a>

## Test log

ROS/hardware results have not been recorded yet. After each run, fill in the tested commit, actual ports, gains and observations.

| Task | Date / tester / commit | Result | Notes and evidence |
| --- | --- | --- | --- |
| D3.1.0 | | Not run | |
| D3.1.1 | | Not run | |
| D3.2 | | Not run | |

<a id="d3-evidence"></a>

## Evidence

Save screenshots and small text files in the matching subtask folder, for example `deliverables/D3/D3.1.0/graph.png`. Add filenames or links to the test table. Keep large videos and bags in the agreed course storage and link them here.

Submission date / course upload link / demonstration: not recorded.

</details>

<a id="d4"></a>

<details>
<summary>D4 - RViz visualization</summary>

Use a separate terminal for each running node or recorder. In every terminal, source Jazzy and the workspace as shown in the root README. Record bags before the demonstration and close the recorder with Ctrl+C.

## Units and position estimate

TF is `world -> group_7/stm_station -> group_7/motor`. Station translation comes from IMU acceleration; motor rotation comes from encoder position. Motor rotation is not the orientation of the IMU body.

The template specifies 24 encoder ticks per motor revolution and a gear ratio of 9.7. Yaw is `ticks * 2*pi / (24*9.7)`. Check tick decoding on the device; set encoder_direction=-1.0 if needed.

Keep the station still for the first 50 samples to calibrate acceleration offset. Default acceleration_scale=1.0 assumes m/s^2; use 9.81 if firmware reports g. These settings are in serial_params.yaml. Integration uses sample timestamps; duplicate stamps are skipped, and time reversal or gaps over 0.2 seconds clear velocity without integrating the gap.

A 0.5 m/s^2 deadband filters small corrected accelerations. Existing velocity still contributes to position. The estimate drifts and does not compensate changing gravity direction when the station tilts. Keep sensor axes fixed during translation tests. Reset while stationary to clear position/path and recalibrate. The path keeps at most 1000 samples.

<a id="d4-1"></a>

## D4.1 - TF and RViz

**Prerequisites:** D1.3 working; stationary STM for startup calibration. Stop any previous bridge, or set start_serial:=false.

Start visualization, keep the device still for the first 50 samples, then rotate the motor and translate without tilting. Confirm encoder and acceleration units from firmware.

**Terminal A:** Launch bridge, TF/Path node and saved RViz view.

```bash
ros2 launch stm_station stm_visualization_launch.py group_id:=7 port:=/dev/ttyACM0
```

**Terminal B:** Inspect body TF; Ctrl+C before inspecting motor TF.

```bash
ros2 run tf2_ros tf2_echo world group_7/stm_station
# After Ctrl+C:
ros2 run tf2_ros tf2_echo group_7/stm_station group_7/motor
```

**Terminal C:** Inspect position, reset while stationary, and confirm reset response.

```bash
ros2 topic echo /group_7/stm_position --once
ros2 service call /group_7/reset_visualization std_srvs/srv/Trigger "{}"
```

**Expected:** Connected world -> group_7/stm_station -> group_7/motor frames; encoder-driven motor yaw; bounded trajectory. Reset returns success=true, clears translation/path and recalibrates. Acceleration integration drifts; changing tilt is not compensated.

**Stop:** Ctrl+C TF echo and launch. If bridge was started separately, terminate it when finished. Visualization itself sends no motor commands.

**Save:** RViz view, rotation scaling/sign measurement, calibration/reset observations, actual config/units and movement video. Save results and links in the matching subtask folder under `deliverables/D4/`.

<a id="d4-2"></a>

## D4.2 - Plots and recording

**Prerequisites:** D4.1 running, calibrated and units confirmed.

Record first, then capture an axis-motion and motor-rotation demonstration. Keep the station level; measure stationary drift and describe limitations.

**Terminal B:** Record state, estimates, path and transforms.

```bash
ros2 bag record -o bags/d4_run01 /group_7/stm_state /group_7/stm_position /group_7/stm_velocity /group_7/stm_path /tf /tf_static
```

**Terminal C:** Plot estimated translation.

```bash
ros2 run rqt_plot rqt_plot /group_7/stm_position/point/x /group_7/stm_position/point/y /group_7/stm_position/point/z
```

**Terminal D:** Save actual configuration; open graph.

```bash
mkdir -p deliverables/D4/D4.2
ros2 param dump /group_7/stm_visualization_node > deliverables/D4/D4.2/parameters.yaml
rqt_graph
```

**Expected:** Position curves and TF/Path correspond to the same timestamped state stream. Document drift instead of claiming absolute accuracy.

**Stop:** Ctrl+C recorder, then run `ros2 bag info bags/d4_run01 > deliverables/D4/D4.2/bag-info.txt`. Close plots/graph and stop D4 launch.

**Save:** Plot and RViz screenshots, graph, parameters.yaml, bag-info.txt, video and linked bag. Physical evidence is not collected yet. Save results and links in the matching subtask folder under `deliverables/D4/`.

## Course slides and templates

Current slides refer to Athens2026_ROS2.pptx; older slides refer to Athens_ROS2_Course.pptx. A star marks an extension task.

| Task | Current slides | Older slides | Original template |
| --- | --- | --- | --- |
| D4.1 / D4.2 | 112 | 132 | [11_stm_visualization.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/11_stm_visualization.py) |

<a id="d4-test-log"></a>

## Test log

ROS/hardware results have not been recorded yet. After each run, fill in the tested commit, actual ports, gains and observations.

| Task | Date / tester / commit | Result | Notes and evidence |
| --- | --- | --- | --- |
| D4.1 | | Not run | |
| D4.2 | | Not run | |

<a id="d4-evidence"></a>

## Evidence

Save screenshots and small text files in the matching subtask folder, for example `deliverables/D4/D4.1/graph.png`. Add filenames or links to the test table. Keep large videos and bags in the agreed course storage and link them here.

Submission date / course upload link / demonstration: not recorded.

</details>

<a id="d5"></a>

<details>
<summary>D5 - Robot navigation</summary>

Use a separate terminal for each running node or recorder. In every terminal, source Jazzy and the workspace as shown in the root README. Record bags before the demonstration and close the recorder with Ctrl+C.

## What is ready

The simulation Bug0 controller is implemented. Gazebo verification, real Galileo tests and the separate STM-to-velocity mapping still need work. The sections below explain what can be run and what still needs implementing.

<a id="d5-1-simulation"></a>

## D5.1-simulation - Bug0 in Gazebo

Current Athens2026_ROS2.pptx slides 122/124/125: course Galileo simulator and Bug0 demonstration. Original scaffold: [13_bug0_lidar_stm.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/13_bug0_lidar_stm.py), upstream cf9e122904ebcb55d336aa7e82d0760bc94cbb07, retained unchanged.

The controller is implemented; it still needs a run in Gazebo. Code:

- [bug0.py](src/stm_station/stm_station/bug0.py): sector extraction, reactive decisions and watchdog.
- [bug0_node.py](src/stm_station/stm_station/bug0_node.py): LaserScan subscription, TwistStamped output, optional STM output and enable service.
- [stm_bug0_launch.py](src/stm_station/launch/stm_bug0_launch.py) and [bug0_params.yaml](src/stm_station/config/bug0_params.yaml).

### Actual simulator interface

The course simulator repository is [simulation_ATHENS2026_st](https://github.com/sergiolopezcb/simulation_ATHENS2026_st), inspected at `c70103a97268658b0ee562944996b9294b9599cd`. Its [launch](https://github.com/sergiolopezcb/simulation_ATHENS2026_st/blob/c70103a97268658b0ee562944996b9294b9599cd/sim_galileo_gazebo/launch/robot_simulation.launch.py) starts diff_drive_controller and can disable teleop_gui. Its [controller configuration](https://github.com/sergiolopezcb/simulation_ATHENS2026_st/blob/c70103a97268658b0ee562944996b9294b9599cd/sim_galileo_description/config/ros2_controllers.yaml) sets a 0.5 s velocity timeout.

The [Jazzy controller interface](https://control.ros.org/jazzy/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html) subscribes to ~/cmd_vel as TwistStamped, so our default is `/diff_drive_controller/cmd_vel`. The simulator also contains a `/cmd_vel` Twist bridge and a teleop remap to cmd_vel_unstamped; these are not the selected stamped controller endpoint. Check the actual subscriber and type on your VM before enabling. Defaults: `/scan` LaserScan; `/diff_drive_controller/cmd_vel` TwistStamped; `/diff_drive_controller/odom` Odometry. The inspected lidar mount has zero yaw relative to the robot, which this sector interpretation assumes.

### Behavior and limits

- 10 Hz commands; 0.3 m/s forward, 0.5 rad/s turning (configurable).
- Front +/-30 degrees, left 30..90, right -90..-30, derived from LaserScan angles, not equal chunks of a 360-degree array. Rear returns do not masquerade as front obstacles.
- Front >1.0 m: forward. Otherwise choose the freer side (tie: left) and turn in place. Retain that turn until front >1.2 m; this hysteresis reduces switching. Side clearance below 0.4 m stops. This may stop in narrow spaces rather than complete navigation.
- +inf means no return up to range_max. NaN/invalid high samples are unknown; less than 50% valid samples in any required sector stops. Too-close/negative-infinite ranges conservatively count as zero clearance.
- Starts disabled; `/group_7/bug0_enable` SetBool enables only with a fresh complete scan. `false` immediately publishes zero.
- Missing, invalid or stale scans stop/disarm; explicit re-enable is required. Header age and receive timeout are checked; the steady-clock timer also runs while simulator time is paused. Unstamped manual test scans use receive age only. State is published on `/group_7/bug0_state`.
- Optional `enable_stm:=true` publishes mode-2 PWM (forward 90, turn +/-70) to `/group_7/stm_control`, with stop mode 0. Default is false: pure simulation needs no STM device. No other STM controller/publisher may command that station concurrently.

This follows the course's simple Bug0-style obstacle avoidance exercise. There is no goal input, goal-seeking odometry or complete boundary-following planner, and no claim of reaching arbitrary goals or navigating every obstacle layout.

### Simulator setup (only if not already installed)

Run from the team repository root on the course VM. The external clone is ignored by Git; it is not a team solution or vendored template.

```bash
source /opt/ros/jazzy/setup.bash
# Only if src/simulation_ATHENS2026_st does not exist:
git clone https://github.com/sergiolopezcb/simulation_ATHENS2026_st.git src/simulation_ATHENS2026_st
git -C src/simulation_ATHENS2026_st checkout c70103a97268658b0ee562944996b9294b9599cd
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

If the course simulator is already built in another workspace, source that workspace before the team overlay instead of cloning another copy. `ros2 pkg prefix sim_galileo_gazebo` checks availability.

### Run in Gazebo

Source Jazzy and the workspace in each terminal. Keep teleoperation and any other velocity publisher off.

Terminal A:

```bash
ros2 launch sim_galileo_gazebo robot_simulation.launch.py use_teleop_gui:=false
```

Terminal B, after the robot/controllers and scans appear:

```bash
ros2 topic info /scan -v
ros2 topic info /diff_drive_controller/cmd_vel -v
ros2 control list_controllers
ros2 launch stm_station stm_bug0_launch.py group_id:=7
```

Terminal C, start recording BEFORE enabling movement:

```bash
ros2 bag record -o bags/d5_1_sim_run01 /scan /diff_drive_controller/cmd_vel /diff_drive_controller/odom /group_7/bug0_state /clock
```

Terminal D:

```bash
ros2 service call /group_7/bug0_enable std_srvs/srv/SetBool "{data: true}"
ros2 topic echo /group_7/bug0_state --once
ros2 param dump /group_7/bug0_lidar_stm_node > deliverables/D5/D5.1-simulation/parameters.yaml
# Disable and command zero before cleanup:
ros2 service call /group_7/bug0_enable std_srvs/srv/SetBool "{data: false}"
```

Enable response is success=true only once usable scans arrive. A clear front produces forward; a blocked front produces a left/right turn; sufficient front clearance resumes forward. Move/place obstacles in Gazebo and record separate clear, blocked-left/right and resumed-motion cases. The controller can stop for insufficient side clearance. To check scan loss, pause the simulation for >0.5 s: the steady-time watchdog disarms; unpause and explicitly re-enable after scans resume. Verify the state and zero command, rather than treating simulator pause as physical stop evidence.

Disable first; Ctrl+C recorder, Bug0 launch, then simulator. The final shutdown zero is best effort; normal cleanup uses the explicit disable service. The external controller's configured timeout handles command loss. Then:

```bash
ros2 bag info bags/d5_1_sim_run01 > deliverables/D5/D5.1-simulation/bag-info.txt
```

The Terminal D parameter dump is taken while the node is running. Save `D5.1-simulation_graph.png`, `D5.1-simulation_obstacle.png`, transcript, config, bag-info and an accessible video/bag link in the evidence section below. Actual simulation results are still NOT RUN here.

### Isolated ROS check without Gazebo or hardware

This checks the actual node using synthetic scans and isolated output topics. It needs ROS but no simulator. Do not combine with a live /scan producer.

Terminal A:

```bash
ros2 launch stm_station stm_bug0_launch.py use_sim_time:=false scan_topic:=/group_7/test_scan cmd_vel_topic:=/group_7/test_cmd_vel
```

Terminal B, repeated clear scan (zero header deliberately uses receive time):

```bash
ros2 topic pub --rate 5 /group_7/test_scan sensor_msgs/msg/LaserScan "{angle_min: -1.5707963, angle_increment: 0.5235988, range_min: 0.3, range_max: 12.0, ranges: [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]}"
```

Terminal C:

```bash
ros2 service call /group_7/bug0_enable std_srvs/srv/SetBool "{data: true}"
ros2 topic echo /group_7/test_cmd_vel --once
```

Expected: linear.x=0.3, angular.z=0. Stop Terminal B with Ctrl+C and wait >0.6 s; Terminal C echo must show zeros and bug0_state must be disabled. Restart scans and explicitly enable again.

For a left-turn case stop the old publisher, let the watchdog disarm, then publish the same scan with ranges `[1.0, 1.0, 1.0, 0.6, 5.0, 5.0, 5.0]` and enable. Expect linear.x=0, angular.z=+0.5. Reverse side values for a right-turn case, with disable/re-enable between tests. Disable and Ctrl+C all test terminals after finishing. Synthetic results are not Gazebo or physical evidence.

<a id="d5-1-real"></a>

## D5.1-real - Real Galileo Bug0 (hardware testing pending)

**Prerequisites:** Simulation task passed and real robot bringup available.

Port the tested Bug0 controller to the actual robot topics/units and course speed limits. The simulation Bug0 controller is available; real-robot bringup and verified hardware configuration are not supplied yet.

**Terminal A:** After course bringup, inspect actual interfaces only. These commands do not launch a robot or a missing solution.

```bash
ros2 topic list -t
ros2 topic info /cmd_vel -v
```

**Expected:** A future physical test must demonstrate repeatable avoidance and stop behavior; simulation evidence is insufficient.

**Stop:** No solution is started by this section. When testing future code, command zero velocity through the confirmed robot interface and stop recorder/controller/bringup according to the course robot instructions.

**Save:** Prepare the linked test/evidence pages now; leave them NOT RUN. After implementation upload the task-specific video/bag and save graph, actual commands, robot version, topic types, limits and observations. Save results and links in the matching subtask folder under `deliverables/D5/`.

<a id="d5-2"></a>

## D5.2 - STM to simulated robot (not implemented)

**Prerequisites:** Course simulator and verified STM velocity/gyro units.

Implement/register stm_turtlebot_control from reference/templates/12_stm_turtlebot_control.py. Map motor_velocity to linear.x and gyro to angular.z with scaling, limits and stale-state stop. Do not run the unfinished reference template.

**Terminal A:** After course bringup, inspect actual interfaces only. These commands do not launch a robot or a missing solution.

```bash
ros2 topic list -t
ros2 topic info /cmd_vel -v
```

**Expected:** Future tests must demonstrate both speed axes and stale-input stop. Current slide 133 repeats this task, not a second completed assignment.

**Stop:** No solution is started by this section. When testing future code, command zero velocity through the confirmed robot interface and stop recorder/controller/bringup according to the course robot instructions.

**Save:** Prepare the linked test/evidence pages now; leave them NOT RUN. After implementation upload the task-specific video/bag and save graph, actual commands, robot version, topic types, limits and observations. Save results and links in the matching subtask folder under `deliverables/D5/`.

<a id="d5-real-stm"></a>

## D5-real-stm - STM to real robot (not implemented)

**Prerequisites:** D5.2 verified plus course real-robot bringup.

Adapt the completed mapping to the actual robot and verify physical response and loss-of-input stop. No runnable solution is available yet.

**Terminal A:** After course bringup, inspect actual interfaces only. These commands do not launch a robot or a missing solution.

```bash
ros2 topic list -t
ros2 topic info /cmd_vel -v
```

**Expected:** Future tests must demonstrate real forward/turn control and stop behavior, with separate physical evidence.

**Stop:** No solution is started by this section. When testing future code, command zero velocity through the confirmed robot interface and stop recorder/controller/bringup according to the course robot instructions.

**Save:** Prepare the linked test/evidence pages now; leave them NOT RUN. After implementation upload the task-specific video/bag and save graph, actual commands, robot version, topic types, limits and observations. Save results and links in the matching subtask folder under `deliverables/D5/`.

## Course slides and templates

Current slides refer to Athens2026_ROS2.pptx; older slides refer to Athens_ROS2_Course.pptx. A star marks an extension task.

| Task | Current slides | Older slides | Original template |
| --- | --- | --- | --- |
| D5.1 simulation | 125 | - | [13_bug0_lidar_stm.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/13_bug0_lidar_stm.py) |
| D5.1 real | 128 | - | [13_bug0_lidar_stm.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/13_bug0_lidar_stm.py) |
| D5.2* | 129; repeated at 133 | 143 | [12_stm_turtlebot_control.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/12_stm_turtlebot_control.py) |
| D5 real STM* | 130 | - | [12_stm_turtlebot_control.py](https://github.com/Robolabo/ROS_course/blob/cf9e122904ebcb55d336aa7e82d0760bc94cbb07/Templates/12_stm_turtlebot_control.py) |

The current slides use D5.1 for both simulation and real Bug0. Slide 133 repeats the STM simulation task from 129. Record their test results separately.

<a id="d5-test-log"></a>

## Test log

ROS/hardware results have not been recorded yet. After each run, fill in the tested commit, actual ports, gains and observations.

| Task | Date / tester / commit | Result | Notes and evidence |
| --- | --- | --- | --- |
| D5.1-simulation | | Not run | |
| D5.1-real | | Not run | |
| D5.2 | | Not run | |
| D5-real-stm | | Not run | |

<a id="d5-evidence"></a>

## Evidence

Save screenshots and small text files in the matching subtask folder, for example `deliverables/D5/D5.1-simulation/graph.png`. Add filenames or links to the test table. Keep large videos and bags in the agreed course storage and link them here.

Submission date / course upload link / demonstration: not recorded.

</details>
