Name:           ros-kinetic-rosconsole_bridge
Version:        0.5.1
Release:        3%{?dist}
Summary:        ROS package rosconsole_bridge

License:        BSD
URL:            http://www.ros.org/wiki/rosconsole_bridge

Source0:        https://github.com/ros-gbp/rosconsole_bridge-release/archive/release/kinetic/rosconsole_bridge/0.5.1-0.tar.gz#/ros-kinetic-rosconsole_bridge-0.5.1-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python2-devel

BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  log4cxx-devel
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-rosconsole

Requires:       ros-kinetic-rosconsole

%description
rosconsole_bridge is a package used in conjunction with console_bridge
and rosconsole for connecting console_bridge-based logging to
rosconsole-based logging.


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
  --pkg rosconsole_bridge

rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,setup*,env.sh}

find %{buildroot}/%{_libdir}/ros/{bin,etc,include,lib/pkgconfig,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list


find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list

%files -f files.list



%changelog
* Mon Nov 20 2017 Till Hofmann <thofmann@fedoraproject.org> - 0.5.1-3
- Add missing BR on boost-devel
* Mon Nov 20 2017 Till Hofmann <thofmann@fedoraproject.org> - 0.5.1-2
- Add missing BR on log4cxx-devel
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 0.5.1-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.4.4-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 0.4.4-1
- Update auto-generated Spec file
