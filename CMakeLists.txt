cmake_minimum_required(VERSION 2.8.3)

project(gantry_assembly_v2)

find_package(catkin REQUIRED COMPONENTS
			rospy
			roscpp
			std_msgs
			gazebo_ros
			message_generation)



find_package(gazebo REQUIRED)

add_service_files(
  FILES
  Attach.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(CATKIN_DEPENDS message_runtime)

include_directories(include)
link_directories(${GAZEBO_LIBRARY_DIRS})
include_directories(${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS})

add_library(${PROJECT_NAME} src/gantry_assembly_v2.cpp) 

target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})
add_dependencies(${PROJECT_NAME} ${${PROJECT_NAME}_EXPORTED_TARGETS})



foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)


