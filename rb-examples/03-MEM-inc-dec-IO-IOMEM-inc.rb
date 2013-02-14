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
				:href => "/distributions/linear",
				:name => "linear"},
	        :startLoad => "1000",
       		:stopLoad => "20000",
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
                :startLoad => "20000",
                :stopLoad => "20000",
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
                                :href => "/distributions/linear",
                                :name => "linear"},
                :startLoad => "1000",
                :stopLoad => "20000",
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
                                :href => "/distributions/linear",
                                :name => "linear"},
                :startLoad => "100",
                :stopLoad => "100",
                :emulator =>{
                                :href => "/emulators/stressapptest",
                                :name => "stressapptest"},
                :'emulator-params' =>{
                                :resourceType =>"IO",
                                :fileQty => "20",
				:memThreads => "1"}
                },
		{
                :name => "IO-MEM-inc",
                :startTime =>"541",
                :duration =>"239",
                :granularity =>"20",
                :distribution => {
                                :href => "/distributions/linear",
                                :name => "linear"},
                :startLoad => "1000",
                :stopLoad => "20000",
                :emulator =>{
                                :href => "/emulators/stressapptest",
                                :name => "stressapptest"},
                :'emulator-params' =>{
                                :resourceType =>"IO",
                                :fileQty => "20",
				:memThreads => "5"}
                }]
 )
               
end
