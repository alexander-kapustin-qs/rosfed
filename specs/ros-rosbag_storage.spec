Name:           ros-rosbag_storage
Version:        noetic.1.15.13
Release:        2%{?dist}
Summary:        ROS package rosbag_storage

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/ros_comm-release/archive/release/noetic/rosbag_storage/1.15.13-1.tar.gz#/ros-noetic-rosbag_storage-1.15.13-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  boost-devel
BuildRequires:  bzip2-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gpgme-devel
BuildRequires:  lz4-devel
BuildRequires:  openssl-devel
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-cpp_common-devel
BuildRequires:  ros-noetic-pluginlib-devel
BuildRequires:  ros-noetic-roscpp_serialization-devel
BuildRequires:  ros-noetic-roscpp_traits-devel
BuildRequires:  ros-noetic-roslz4-devel
BuildRequires:  ros-noetic-rostest-devel
BuildRequires:  ros-noetic-rostime-devel
BuildRequires:  ros-noetic-std_msgs-devel

Requires:       ros-noetic-cpp_common
Requires:       ros-noetic-pluginlib
Requires:       ros-noetic-roscpp_serialization
Requires:       ros-noetic-roscpp_traits
Requires:       ros-noetic-roslz4
Requires:       ros-noetic-rostime

Provides:  ros-noetic-rosbag_storage = 1.15.13-2
Obsoletes: ros-noetic-rosbag_storage < 1.15.13-2
Obsoletes: ros-kinetic-rosbag_storage < 1.15.13-2



%description
This is a set of tools for recording from and playing back ROS message
without relying on the ROS client library.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       boost-devel
Requires:       bzip2-devel
Requires:       console-bridge-devel
Requires:       gpgme-devel
Requires:       lz4-devel
Requires:       openssl-devel
Requires:       ros-noetic-cpp_common-devel
Requires:       ros-noetic-pluginlib-devel
Requires:       ros-noetic-roscpp_serialization-devel
Requires:       ros-noetic-roscpp_traits-devel
Requires:       ros-noetic-roslz4-devel
Requires:       ros-noetic-rostest-devel
Requires:       ros-noetic-rostime-devel
Requires:       ros-noetic-std_msgs-devel

Provides: ros-noetic-rosbag_storage-devel = 1.15.13-2
Obsoletes: ros-noetic-rosbag_storage-devel < 1.15.13-2
Obsoletes: ros-kinetic-rosbag_storage-devel < 1.15.13-2


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
  --pkg rosbag_storage




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/rosbag_storage/cmake} \
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
* Thu Oct 14 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.13-2
- Rebuild to pull in updated dependencies
* Thu Oct 14 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.13-1
- Update to latest release
* Mon May 17 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.11-1
- Update to latest release
* Thu Apr 08 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.10-1
- Update to latest release
* Tue Feb 23 2021 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.9-2
- Modernize python shebang replacement
* Mon Nov 02 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.9-1
- Update to latest release
* Sat Aug 08 2020 Nicolas Limpert - noetic.1.15.8-1
- Update to latest release
* Thu Jun 11 2020 Nicolas Limpert - noetic.1.15.7-1
- Update to latest release
* Sun May 24 2020 Till Hofmann <thofmann@fedoraproject.org> - noetic.1.15.6-1
- Upgrade to noetic
* Fri Apr 17 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.14.5-1
- Update to latest release
* Wed Mar 04 2020 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.14.4-1
- Update to latest release
* Mon Jul 22 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.14.3-3
- Remove obsolete python2 dependencies
* Sun Jul 21 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.14.3-2
- Switch to python3
* Sat Jul 13 2019 Till Hofmann <thofmann@fedoraproject.org> - melodic.1.14.3-1
- Update to ROS melodic release
* Fri Jul 12 2019 Till Hofmann <thofmann@fedoraproject.org> - 1.12.14-2
- Remove ROS distro from package name
* Wed Nov 07 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.14-1
- Update to latest release
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.13-5
- devel also requires: the devel package of each run dependency
* Tue May 22 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.13-4
- devel also requires: the devel package of each run dependency
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.13-3
- Also add upstream's exec_depend as Requires:
* Tue May 15 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.13-2
- Add corresponding devel Requires: for the package's BRs and Rs
* Mon May 14 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.13-1
- Update to latest release, rebuild for F28
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-6
- Replace Recommends: with Requires: in devel subpackage
* Tue Feb 20 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-5
- Fix Requires: in devel subpackage
* Mon Feb 19 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-4
- Add Recommends: for all BRs to the devel subpackage
* Tue Feb 06 2018 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-3
- Split devel package
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-2
- Add missing BR on lz4-devel
* Sun Nov 19 2017 Till Hofmann <thofmann@fedoraproject.org> - 1.12.12-1
- Update to latest release
* Fri Aug 25 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.7-2
- Remove all Requires: on devel packages
* Wed Aug 16 2017 Till Hofmann <hofmann@kbsg.rwth-aachen.de> - 1.12.7-1
- Update auto-generated Spec file
