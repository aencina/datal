# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.

  # Maquina Virtual Ubuntu Trusty
  config.vm.box = "ubuntu/trusty64"

  # Maquina Virtual Debian 8.2
  # config.vm.box = "boxcutter/debian82"

  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.

  config.vm.network "forwarded_port", guest: 80, host: 8080 # NGINX
  config.vm.network "forwarded_port", guest: 3016, host: 8016 # Admin
  config.vm.network "forwarded_port", guest: 3018, host: 8018 # API
  config.vm.network "forwarded_port", guest: 3017, host: 8017 # Microsite
  config.vm.network "forwarded_port", guest: 3015, host: 8015 # Workspace Application
  config.vm.network "forwarded_port", guest: 3306, host: 8306 # MySQL
  config.vm.network "forwarded_port", guest: 8080, host: 8081 # Tomcat
  config.vm.network "forwarded_port", guest: 8888, host: 8888 # Datstore

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder ".", "/home/vagrant/app", :group =>'vagrant', :owner => 'vagrant'
  config.vm.synced_folder "salt/pillar/", "/srv/salt/pillar/"

  # Salt provisioning
  config.vm.provision :salt do |salt|
    salt.minion_config = "salt/minion"
    salt.run_highstate = true
    salt.verbose = true
    salt.colorize = true
    salt.bootstrap_options = '-P'
  end
  if Vagrant.has_plugin?("vagrant-proxyconf")
    config.proxy.http     = "http://proxy2:8082/"
    config.proxy.https    = "http://proxy2:8082/"
    config.proxy.no_proxy = "localhost,127.0.0.1,.example.com"
  end
end
