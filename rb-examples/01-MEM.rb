require 'rubygems'
require 'restfully'
require 'logger'

session = Restfully::Session.new(
 :configuration_file => ".restfully/api.cocoma.yml"

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
   :distributions => {
   		:name => "MEM-increase",
           	:startTime =>"5",
       		:duration =>"110",        
       		:granularity =>"10",
	        :distribution => {
				:href => "/distributions/linear",
				:name => "linear"},
	        :startLoad => "10%",
       		:stopLoad => "80%",
		:malloclimit => 4095,
       		:emulator =>{
				:href => "/emulators/stressapptest",
				:name => "stressapptest"},
       		:'emulator-params' =>{
           			:resourceType =>"MEM",
           			:memThreads => "5"}
		}
 )
               
end
