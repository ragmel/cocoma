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
   :emuName => "CPU-emulation",
   :emuType => "Contention",
   :emuResourceType => "CPU",
   :emuStartTime => "now",
   :emuStopTime => "240",
   :distributions =>[{
   		:name => "CPU-increase",
           	:startTime =>"0",
       		:duration =>"120",        
       		:granularity =>"8",
	        :distribution => {
				:href => "/distributions/linear",
				:name => "linear"},
	        :startLoad => "10",
       		:stopLoad => "90",
       		:emulator =>{
				:href => "/emulators/lookbusy",
				:name => "lookbusy"},
       		:'emulator-params' =>{
           			:resourceType =>"CPU",
           			:ncpus => "6"}
		},
    		{
                :name => "CPU-decrease",
                :startTime =>"121",
                :duration =>"119",
                :granularity =>"8",
                :distribution => {
                                :href => "/distributions/linear",
                                :name => "linear"},
                :startLoad => "90",
                :stopLoad => "10",
                :emulator =>{
                                :href => "/emulators/lookbusy",
                                :name => "lookbusy"},
                :'emulator-params' =>{
                                :resourceType =>"CPU",
                                :ncpus => "6"}
                }]
 )
               
end
