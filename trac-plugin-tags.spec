%define		trac_ver	0.12
%define		plugin		tags
Summary:	Add simple support for renaming/moving wiki pages
Name:		trac-plugin-%{plugin}
Version:	0.6
Release:	0.3
License:	BSD
Group:		Applications/WWW
# Source0Download:	http://trac-hacks.org/changeset/latest/tagsplugin/tags/0.6?old_path=/&filename=tagsplugin/tags/0.6&format=zip
Source0:	http://trac-hacks.org/changeset/latest/tagsplugin/tags/0.6?old_path=/&filename=tagsplugin/tags/0.6&format=zip
# Source0-md5:	82c5dead1f61c82ea1f6a023ca612a77
#Source0:	%{plugin}-%{version}.zip
Patch0:		pysqlite.patch
URL:		http://trac-hacks.org/wiki/TagsPlugin
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This plugin allows you to rename wiki pages. It is an evolution of the
WikiRenameScript, and currently has the same limitations.

It will move a page and its history, and will rewrite explicit links
[wiki:PageName Label] leading to it from other wiki pages. It will
also move any attachments on the page.

caution: Currently this plugin doesn't interact well with the
TagsPlugin. You should be careful to remove any tags on a page before
renaming it, and then re-adding them to the new page.

You can access the page rename form through the Admin system. For
convenience, a link is also added to the context navigation bar in the
wiki.

%prep
%setup -q -n %{plugin}plugin
%patch0 -p1

%build
cd %{plugin}/%{version}
%{__python} setup.py build
%{__python} setup.py egg_info

%install
rm -rf $RPM_BUILD_ROOT
cd %{plugin}/%{version}
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	%banner -e %{name} <<-'EOF'
	To enable the %{plugin} plugin, add to conf/trac.ini:

	[components]
	trac%{plugin}.* = enabled
EOF
fi

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/trac%{plugin}
%{py_sitescriptdir}/TracTags-*.egg-info
