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
   :emuStopTime => "780",
   :distributions =>[{
   		:name => "MEM-increase",
           	:startTime =>"0",
       		:duration =>"120",        
       		:granularity =>"20",
	        :distribution => {
				:href => "/distributions/linear_incr",
				:name => "linear_incr"},
	        :startLoad => "10%",
       		:stopLoad => "80%",
		:malloclimit => 4095,
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
                                :href => "/distributions/linear_incr",
                                :name => "linear_incr"},
                :startLoad => "80%",
                :stopLoad => "80%",
		:malloclimit => 4095,
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
                :granularity =>"20",
                :distribution => {
                                :href => "/distributions/linear_icnr",
                                :name => "linear_incr"},
                :startLoad => "80%",
                :stopLoad => "10%",
		:malloclimit => 4095,
                :emulator =>{
                                :href => "/emulators/stressapptest",
                                :name => "stressapptest"},
                :'emulator-params' =>{
                                :resourceType =>"MEM",
                                :memThreads => "10"}
                },
		{
                :name => "IO",
                :startTime =>"301",
                :duration =>"239",
                :granularity =>"1",
                :distribution => {
                                :href => "/distributions/linear_incr",
                                :name => "linear_incr"},
                :startLoad => "1",
                :stopLoad => "20",
                :emulator =>{
                                :href => "/emulators/stressapptest",
                                :name => "stressapptest"},
                :'emulator-params' =>{
                                :resourceType =>"IO",
                                :memsize => "1000",
				:memThreads => "10"}
                }]
 )
               
end
