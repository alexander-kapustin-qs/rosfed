Name:           ros-laser_filters
Version:        noetic.1.9.0
Release:        1%{?dist}
Summary:        ROS package laser_filters

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/laser_filters-release/archive/release/noetic/laser_filters/1.9.0-1.tar.gz#/ros-noetic-laser_filters-1.9.0-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  eigen3-devel
BuildRequires:  poco-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  ros-noetic-angles-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-dynamic_reconfigure-devel
BuildRequires:  ros-noetic-filters-devel
BuildRequires:  ros-noetic-laser_geometry-devel
BuildRequires:  ros-noetic-message_filters-devel
BuildRequires:  ros-noetic-nodelet-devel
BuildRequires:  ros-noetic-pluginlib-devel
BuildRequires:  ros-noetic-roscpp-devel
BuildRequires:  ros-noetic-rostest-devel
BuildRequires:  ros-noetic-sensor_msgs-devel
BuildRequires:  ros-noetic-tf-devel

Requires:       ros-noetic-angles
Requires:       ros-noetic-dynamic_reconfigure
Requires:       ros-noetic-filters
Requires:       ros-noetic-laser_geometry
Requires:       ros-noetic-message_filters
Requires:       ros-noetic-nodelet
Requires:       ros-noetic-pluginlib
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-sensor_msgs
Requires:       ros-noetic-tf

Provides:  ros-noetic-laser_filters = 1.9.0-1
Obsoletes: ros-noetic-laser_filters < 1.9.0-1
Obsoletes: ros-kinetic-laser_filters < 1.9.0-1



%description
Assorted filters designed to operate on 2D planar laser scanners,
which use the sensor_msgs/LaserScan type.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       eigen3-devel
Requires:       poco-devel
Requires:       tinyxml-devel
Requires:       tinyxml2-devel
Requires:       ros-noetic-angles-devel
Requires:       ros-noetic-dynamic_reconfigure-devel
Requires:       ros-noetic-filters-devel
Requires:       ros-noetic-laser_geometry-devel
Requires:       ros-noetic-message_filters-devel
Requires:       ros-noetic-nodelet-devel
Requires:       ros-noetic-pluginlib-devel
Requires:       ros-noetic-roscpp-devel
Requires:       ros-noetic-rostest-devel
Requires:       ros-noetic-sensor_msgs-devel
Requires:       ros-noetic-tf-devel

Provides: ros-noetic-laser_filters-devel = 1.9.0-1
Obsoletes: ros-noetic-laser_filters-devel < 1.9.0-1
Obsoletes: ros-kinetic-laser_filters-devel < 1.9.0-1


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

# substitute shebang before install block because we run the local catkin script
%py3_shebang_fix .

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  -DPYTHON_VERSION=%{python3_version} \
  -DPYTHON_VERSION_NODOTS=%{python3_version_nodots} \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg laser_filters




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/laser_filters/cmake} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files_devel.list

find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list



# replace cmake python macro in shebang
for file in $(grep -rIl '^#!.*@PYTHON_EXECUTABLE@.*$' %{buildroot}) ; do
  sed -i.orig 's:^#!\s*@PYTHON_EXECUTABLE@\s*:%{__python3}:' $file
  touch -r $file.orig $file
  rm $file.orig
done


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list

%py3_shebang_fix %{buildroot}

# Also fix .py.in files
for pyfile in $(grep -rIl '^#!.*python.*$' %{buildroot}) ; do
  %py3_shebang_fix $pyfile
done


%files -f files.list
%files devel -f files_devel.list


%changelog
* Wed Nov 24 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.9.0-1
- Update to latest release
* Thu Oct 14 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.8.11-3
- Rebuild to pull in updated dependencies
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.8.11-2
- Modernize python shebang replacement
* Mon Nov 02 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.8.11-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.8.9-1
- Upgrade to noetic
* Fri Apr 17 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.8.10-1
- Update to latest release
* Tue Feb 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.8.8-1
- Update to latest release
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.8.7-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.8.7-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.8.7-1
- Update to ROS melodic release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-8
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-7
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-6
- Also add upstream's exec_depend as Requires:
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-5
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-4
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-3
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-2
- Split devel package
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.8.5-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.8.3-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.8.3-1
- Update auto-generated Spec file
