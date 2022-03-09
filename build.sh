#!/bin/sh

set -xe

#SPEC=specs/ros-geographic_msgs.spec
#SPEC=specs/ros-uuid_msgs.spec
SPEC=specs/ros-ros_comm.spec

spectool -g  $SPEC  -C ~/rpmbuild/SOURCES
rpmbuild -ba $SPEC
