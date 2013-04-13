base_box = ENV['VAGRANT_BOX'] || 'quantal64'
base_box_url = ENV['VAGRANT_BOX_URL'] || 'http://static.aldoborrero.com/vagrant/quantal64.box'

home_path = ENV['HOME']

Vagrant::Config.run do |config|
    config.vm.box = base_box
    config.vm.box_url = base_box_url

    # for best results add "10.10.10.10 app.local"
    # or something like it to your hosts file
    config.vm.network :hostonly, "10.10.10.10"

    # /vagrant is the folder in which the current path is mounted
    # permissions are set so that non-Windows machines won't have
    # to mess with permissions
    config.vm.share_folder("vagrant-root", "/vagrant", ".", :extra => 'dmode=777,fmode=777')

    config.vm.provision :chef_solo do |chef|

        # these settings assume that you have vagrant-chef as
        # a submodule in your app in the vagrant-chef folder
        chef.cookbooks_path = "vagrant-chef/chef/cookbooks"
        chef.data_bags_path = "vagrant-chef/chef/data_bags"

        # for now this mostly runs everything, this needs to be
        # changed so that site-by-site configurations can be made
        # on the Vagrantfile level, not from within cookbooks
        chef.add_recipe "vagrant-main"

        chef.json.merge!({
            "mysql" => {
                "server_root_password" => "password",
                "server_debian_password" => "password",
                "server_repl_password" => "password",
            },
            "sites" => ["default"]
            # you can add databases to a list here
	    # You'll also need to add a trailing comma above
#            "database" => {
#                "create" => ["example_db_name"]
#            }
        })

    end
end

# this section represents laziness, fix with proper chef provisioning
# uncomment a section and set it up as necessary
Vagrant::Config.run do |config|

    config.vm.provision :shell do |shell|
        shell.inline = "cd /vagrant && composer install"
    end
    # import remote database
#    config.vm.provision :shell do |shell|
#        shell.inline = "mysqldump -hhostname -uusername -ppassword databasename > dump.sql && mysql -uroot -ppassword example_db_name < dump.sql"
#    end
    # run Laravel migration
#    config.vm.provision :shell do |shell|
#        shell.inline = "php /vagrant/artisan migrate --env=local"
#    end
    # permissions for the application's storage folder
    config.vm.provision :shell do |shell|
        shell.inline = "chmod 777 -R /vagrant/app/storage"
    end
    # install phpunit (this should be a cookbook)
    config.vm.provision :shell do |shell|
        shell.inline = "sudo apt-get -y install phpunit"
    end
end
