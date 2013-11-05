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
	:name => "MEM-increase",
	:startTime =>"0",
	:duration =>"120",        
	:granularity =>"20",
	:minJobTime => "2",
	:distribution => {
			:href => "/distributions/linear",
			:name => "linear"},
	:startLoad => "50",
	:stopLoad => "500",
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
