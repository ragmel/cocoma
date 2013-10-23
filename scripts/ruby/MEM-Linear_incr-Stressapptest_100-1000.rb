require 'rubygems'
require 'restfully'
require 'logger'

session = Restfully::Session.new(
 :configuration_file => ENV['COCOMA'] + "/scripts/api.cocoma.yml"

)

session.logger.level = Logger::INFO

emulation = nil

begin
 emulation = session.root.emulations.submit(
   :emuName => "MEM_EMU",
   :emuType => "TIME",
   :emuResourceType => "MEM",
   :emuStartTime => "now",
   :emuStopTime => "120",
   :distributions => {
	:name => "MEM-linear_increase",
	:startTime =>"0",
	:duration =>"120",        
	:granularity =>"20",
	:distribution => {
			:href => "/distributions/linear_incr",
			:name => "linear_incr"},
	:startLoad => "100",
	:stopLoad => "1000",
	:emulator =>{
			:href => "/emulators/stressapptest",
			:name => "stressapptest"},
	:'emulator-params' =>{
			:resourceType =>"MEM",
			:malloclimit => 4095,
			:memThreads => "0"}
   },
   :log => {
	:enable => 0,
	:frequency => 3,
	:logLevel => "debug"
   }
 )
               
end
