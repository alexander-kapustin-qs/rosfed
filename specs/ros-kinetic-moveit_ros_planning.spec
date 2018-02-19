Name:           ros-kinetic-moveit_ros_planning
Version:        0.9.11
Release:        1%{?dist}
Summary:        ROS package moveit_ros_planning

License:        BSD
URL:            http://moveit.ros.org

Source0:        https://github.com/ros-gbp/moveit-release/archive/release/kinetic/moveit_ros_planning/0.9.11-0.tar.gz#/ros-kinetic-moveit_ros_planning-0.9.11-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  urdfdom-devel
BuildRequires:  ros-kinetic-actionlib
BuildRequires:  ros-kinetic-angles
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-dynamic_reconfigure
BuildRequires:  ros-kinetic-moveit_core
BuildRequires:  ros-kinetic-moveit_ros_perception
BuildRequires:  ros-kinetic-pluginlib

Requires:       ros-kinetic-actionlib
Requires:       ros-kinetic-angles
Requires:       ros-kinetic-dynamic_reconfigure
Requires:       ros-kinetic-moveit_core
Requires:       ros-kinetic-moveit_ros_perception
Requires:       ros-kinetic-pluginlib

%description
Planning components of MoveIt that use ROS


%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}

%build
# nothing to do here


%install

PYTHONUNBUFFERED=1 ; export PYTHONUNBUFFERED

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS ; \
FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \


source %{_libdir}/ros/setup.bash

DESTDIR=%{buildroot} ; export DESTDIR

catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg moveit_ros_planning

rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,setup*,env.sh}

find %{buildroot}/%{_libdir}/ros/{bin,etc,include,lib*/pkgconfig,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list


find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list

%files -f files.list



%changelog
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.11-1
- Initial package