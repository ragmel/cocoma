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
   :emuStopTime => "300",
   :distributions =>[{
   		:name => "MEM-increase",
           	:startTime =>"0",
       		:duration =>"120",        
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
           			:resourceType =>"MEM",
           			:memThreads => "10"}
		},
		{
                :name => "MEM-stable",
                :startTime =>"121",
                :duration =>"59",
                :granularity =>"1",
                :distribution => {
                                :href => "/distributions/linear",
                                :name => "linear"},
                :startLoad => "18000",
                :stopLoad => "18000",
                :emulator =>{
                                :href => "/emulators/stressapptest",
                                :name => "stressapptest"},
                :'emulator-params' =>{
                                :resourceType =>"MEM",
                                :memThreads => "10"}
                },
    		{
                :name => "MEM-decrease",
                :startTime =>"181",
                :duration =>"119",
                :granularity =>"10",
                :distribution => {
                                :href => "/distributions/linear",
                                :name => "linear"},
                :startLoad => "18000",
                :stopLoad => "1000",
                :emulator =>{
                                :href => "/emulators/stressapptest",
                                :name => "stressapptest"},
                :'emulator-params' =>{
                                :resourceType =>"MEM",
                                :memThreads => "10"}
                }]
 )
               
end
