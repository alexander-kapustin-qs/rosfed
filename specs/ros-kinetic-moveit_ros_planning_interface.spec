Name:           ros-kinetic-moveit_ros_planning_interface
Version:        0.9.11
Release:        1%{?dist}
Summary:        ROS package moveit_ros_planning_interface

License:        BSD
URL:            http://moveit.ros.org

Source0:        https://github.com/ros-gbp/moveit-release/archive/release/kinetic/moveit_ros_planning_interface/0.9.11-0.tar.gz#/ros-kinetic-moveit_ros_planning_interface-0.9.11-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  poco-devel
BuildRequires:  python-catkin_pkg
BuildRequires:  python-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  urdfdom-devel
BuildRequires:  ros-kinetic-actionlib-devel
BuildRequires:  ros-kinetic-catkin-devel
BuildRequires:  ros-kinetic-eigen_conversions-devel
BuildRequires:  ros-kinetic-moveit_resources-devel
BuildRequires:  ros-kinetic-moveit_ros_manipulation-devel
BuildRequires:  ros-kinetic-moveit_ros_move_group-devel
BuildRequires:  ros-kinetic-moveit_ros_planning-devel
BuildRequires:  ros-kinetic-moveit_ros_warehouse-devel
BuildRequires:  ros-kinetic-rosconsole-devel
BuildRequires:  ros-kinetic-roscpp-devel
BuildRequires:  ros-kinetic-rospy-devel
BuildRequires:  ros-kinetic-rostest-devel
BuildRequires:  ros-kinetic-tf-devel
BuildRequires:  ros-kinetic-tf_conversions-devel

Requires:       ros-kinetic-actionlib
Requires:       ros-kinetic-eigen_conversions
Requires:       ros-kinetic-moveit_ros_manipulation
Requires:       ros-kinetic-moveit_ros_move_group
Requires:       ros-kinetic-moveit_ros_planning
Requires:       ros-kinetic-moveit_ros_warehouse
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-roscpp
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-tf
Requires:       ros-kinetic-tf_conversions


%description
Components of MoveIt that offer simpler interfaces to planning and
execution

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python-catkin_pkg
Requires:       ros-kinetic-catkin-devel
Requires:       eigen3-devel
Requires:       fcl-devel
Requires:       poco-devel
Requires:       python-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       urdfdom-devel
Requires:       ros-kinetic-actionlib-devel
Requires:       ros-kinetic-eigen_conversions-devel
Requires:       ros-kinetic-moveit_resources-devel
Requires:       ros-kinetic-moveit_ros_manipulation-devel
Requires:       ros-kinetic-moveit_ros_move_group-devel
Requires:       ros-kinetic-moveit_ros_planning-devel
Requires:       ros-kinetic-moveit_ros_warehouse-devel
Requires:       ros-kinetic-rosconsole-devel
Requires:       ros-kinetic-roscpp-devel
Requires:       ros-kinetic-rospy-devel
Requires:       ros-kinetic-rostest-devel
Requires:       ros-kinetic-tf-devel
Requires:       ros-kinetic-tf_conversions-devel

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.



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
  --pkg moveit_ros_planning_interface




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files_devel.list

find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list


%files -f files.list
%files devel -f files_devel.list


%changelog
* Thu Jan 18 2018 Till Hofmann <thofmann@fedoraproject.org> - 0.9.11-1
- Initial package
