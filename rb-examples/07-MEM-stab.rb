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
   :emuName => "MEM-emulation",
   :emuType => "Contention",
   :emuResourceType => "RAM",
   :emuStartTime => "now",
   :emuStopTime => "120",
   :distributions =>[{
                :name => "MEM-stable",
                :startTime =>"0",
                :duration =>"120",
                :granularity =>"1",
                :distribution => {
                                :href => "/distributions/linear",
                                :name => "linear"},
                :startLoad => "80%",
                :stopLoad => "80%",
		:malloclimit => 4095,
                :emulator =>{
                                :href => "/emulators/stressapptest",
                                :name => "stressapptest"},
                :'emulator-params' =>{
                                :resourceType =>"MEM",
                                :memThreads => "10"}
                }]
 )
               
end
