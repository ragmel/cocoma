require 'rubygems'
require 'restfully'
require 'logger'
#require 'restfully/addons/bonfire'

session = Restfully::Session.new(
 :configuration_file => "~/.restfully/api.cocoma.yml"
# :cache => false,
# :gateway => "ssh.bonfire.grid5000.fr",
# :keys => ["~/.ssh/id_bonfire"]
)

session.logger.level = Logger::INFO

emulation = nil

begin
 emulation = session.root.emulations.submit(
   :emuName => "MEM-IO-emulation",
   :emuType => "Contention",
   :emuResourceType => "Mixed",
   :emuStartTime => "now",
   :emuStopTime => "240",
   :distributions =>[{
                :name => "IO-MEM-inc",
                :startTime =>"0",
                :duration =>"240",
                :granularity =>"10",
                :distribution => {
                                :href => "/distributions/linear",
                                :name => "linear"},
                :startLoad => "1000",
                :stopLoad => "18000",
                :emulator =>{
                                :href => "/emulators/stressapptest",
                                :name => "stressapptest"},
                :'emulator-params' =>{
                                :resourceType =>"IO",
                                :fileQty => "10",
				:memThreads => "1"}
                }]
 )
               
end
