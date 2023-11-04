# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "imu_driver: 1 messages, 1 services")

set(MSG_I_FLAGS "-Iimu_driver:/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg;-Isensor_msgs:/opt/ros/noetic/share/sensor_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(imu_driver_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg" NAME_WE)
add_custom_target(_imu_driver_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "imu_driver" "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg" "sensor_msgs/Imu:geometry_msgs/Quaternion:geometry_msgs/Vector3:sensor_msgs/MagneticField:std_msgs/Header"
)

get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv" NAME_WE)
add_custom_target(_imu_driver_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "imu_driver" "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(imu_driver
  "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Imu.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/MagneticField.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_driver
)

### Generating Services
_generate_srv_cpp(imu_driver
  "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_driver
)

### Generating Module File
_generate_module_cpp(imu_driver
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_driver
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(imu_driver_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(imu_driver_generate_messages imu_driver_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg" NAME_WE)
add_dependencies(imu_driver_generate_messages_cpp _imu_driver_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv" NAME_WE)
add_dependencies(imu_driver_generate_messages_cpp _imu_driver_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(imu_driver_gencpp)
add_dependencies(imu_driver_gencpp imu_driver_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS imu_driver_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(imu_driver
  "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Imu.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/MagneticField.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_driver
)

### Generating Services
_generate_srv_eus(imu_driver
  "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_driver
)

### Generating Module File
_generate_module_eus(imu_driver
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_driver
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(imu_driver_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(imu_driver_generate_messages imu_driver_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg" NAME_WE)
add_dependencies(imu_driver_generate_messages_eus _imu_driver_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv" NAME_WE)
add_dependencies(imu_driver_generate_messages_eus _imu_driver_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(imu_driver_geneus)
add_dependencies(imu_driver_geneus imu_driver_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS imu_driver_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(imu_driver
  "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Imu.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/MagneticField.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_driver
)

### Generating Services
_generate_srv_lisp(imu_driver
  "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_driver
)

### Generating Module File
_generate_module_lisp(imu_driver
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_driver
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(imu_driver_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(imu_driver_generate_messages imu_driver_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg" NAME_WE)
add_dependencies(imu_driver_generate_messages_lisp _imu_driver_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv" NAME_WE)
add_dependencies(imu_driver_generate_messages_lisp _imu_driver_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(imu_driver_genlisp)
add_dependencies(imu_driver_genlisp imu_driver_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS imu_driver_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(imu_driver
  "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Imu.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/MagneticField.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_driver
)

### Generating Services
_generate_srv_nodejs(imu_driver
  "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_driver
)

### Generating Module File
_generate_module_nodejs(imu_driver
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_driver
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(imu_driver_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(imu_driver_generate_messages imu_driver_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg" NAME_WE)
add_dependencies(imu_driver_generate_messages_nodejs _imu_driver_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv" NAME_WE)
add_dependencies(imu_driver_generate_messages_nodejs _imu_driver_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(imu_driver_gennodejs)
add_dependencies(imu_driver_gennodejs imu_driver_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS imu_driver_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(imu_driver
  "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/sensor_msgs/cmake/../msg/Imu.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/opt/ros/noetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/noetic/share/sensor_msgs/cmake/../msg/MagneticField.msg;/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_driver
)

### Generating Services
_generate_srv_py(imu_driver
  "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_driver
)

### Generating Module File
_generate_module_py(imu_driver
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_driver
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(imu_driver_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(imu_driver_generate_messages imu_driver_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/msg/imu_msg.msg" NAME_WE)
add_dependencies(imu_driver_generate_messages_py _imu_driver_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/steffit/Downloads/EECE5554/LAB3/src/imu_driver/srv/convert_to_quaternion.srv" NAME_WE)
add_dependencies(imu_driver_generate_messages_py _imu_driver_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(imu_driver_genpy)
add_dependencies(imu_driver_genpy imu_driver_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS imu_driver_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_driver)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/imu_driver
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(imu_driver_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET sensor_msgs_generate_messages_cpp)
  add_dependencies(imu_driver_generate_messages_cpp sensor_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(imu_driver_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_driver)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/imu_driver
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(imu_driver_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET sensor_msgs_generate_messages_eus)
  add_dependencies(imu_driver_generate_messages_eus sensor_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(imu_driver_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_driver)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/imu_driver
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(imu_driver_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET sensor_msgs_generate_messages_lisp)
  add_dependencies(imu_driver_generate_messages_lisp sensor_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(imu_driver_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_driver)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/imu_driver
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(imu_driver_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET sensor_msgs_generate_messages_nodejs)
  add_dependencies(imu_driver_generate_messages_nodejs sensor_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(imu_driver_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_driver)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_driver\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/imu_driver
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(imu_driver_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET sensor_msgs_generate_messages_py)
  add_dependencies(imu_driver_generate_messages_py sensor_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(imu_driver_generate_messages_py geometry_msgs_generate_messages_py)
endif()
