from board import SCL, SDA
import busio
import time
# Import the SSD1306 module.
import adafruit_ssd1306
import board
import busio
import digitalio


master_ride_id_dict = {
    1222 : "Disney Festival of Fantasy Parade",
    1184 : "A Pirate's Adventure ~ Treasures of the Seven Seas",
    134 : "Jungle Cruise",
    137 : "Pirates of the Caribbean",
    355 : "Swiss Family Treehouse",
    141 : "The Magic Carpets of Aladin",
    334 : "Walt Disney's Enchanted Tiki Room",
    133 : "It's a small world",
    132 : "Dumbo the Flying Elephant",
    128 : "Enchanted Tales with Belle",
    135 : "Mad Tea Party",
    147 : "Meet Ariel at Her Grotto",
    6700 : "Meet Cinderalla",
    144 : "Meet Dairing Disney Pals",
    145 : "Meet Dashing Disney Pals",
    6699 : "Meet Princess Tiana",
    171 : "Mickey's PhilharMagic",
    136 : "Peter Pan's Flight",
    161 : "Prince Charming Regal Carrousel",
    129 : "Seven Dwarfs Mine Train",
    126 : "The Barnstormer",
    142 : "The Many Adventures of Winnie the Pooh",
    127 : "Under the Sea - Journey of The Little Mermaid",
    1181 : "Walt Disney World Railroad - Fantasyland",
    1214 : "Country Bear Jamboree",
    465 : "Tom Sawyer Island",
    1179 : "Walt Disney World Railroad - Frontierland",
    140 : "Haunted Mansion",
    1187 : "Liberty Square Riverboat",
    356 : "The Hall of Presidents",
    1188 : "Main Street Vehicles",
    146 : "Meet Mickey at Town Square Theater",
    1189 : "Walt Disney World Railroad - Main Street, U.S.A",
    248 : "Astro Orbiter",
    131 : "Buzz Lightyear's Space Ranger Spin",
    125 : "Monsters Inc. Laugh Floor",
    138 : "Space Mountain",
    143 : "Tomorrowland Speedway",
    1190 : "Tomorrowland Transit Authority PeopleMover",
    11527 : "TRON Lightcycle Run",
    457 : "Walt Disney's Carousel of Progress",
    13764 : "Casey Jr. Splash 'N' Soak Station",
    13763 : "Cinderella Castle",
    13762 : "Frontierland Shootin' Arcade",
    13750 : "Horses - Disney Animals",
    13630 : "Tiana's Bayou Adventure"
}


MAGIC_KINGDOM_PARK_ID = 0
SCREEN_REFRESH_RATE = 60 #in hz
SCROLLING_SIGN_REFRESH_RATE = 60 #in Hz
SCREEN_REFRESH_PERIOD = 1/SCREEN_REFRESH_RATE
SCROLLING_SIGN_REFRESH_PERIOD = 1/SCROLLING_SIGN_REFRESH_RATE
MAGIC_KINGDOM_STR_CMD = "mkx"
UPDATE_DATA_PERIOD = 300
TIME_PER_RIDE = 15 #seconds per ride

#21 is the length of characters
class RideTitle:
    def __init__(self, ride_title):
        self.master_ride_title = ride_title
        self.master_scrolling_text = ScrollingText(ride_title, 5, 21, 1,SCROLLING_SIGN_REFRESH_PERIOD)
    def run_frame(self, display):
        output_string = self.master_scrolling_text.run_frame()
        display.text(output_string, 0, 0, 1)

class RideData:
    def __init__(self, status, wait_time):
        if(status==False):
            self.status = "Closed"
        else:
            self.status = "Open"
        self.wait_time = wait_time
    def run_frame(self, display):
        display.text("Status: " + self.status, 0, 10, 1)
        display.text("Wait Time: " + str(self.wait_time), 0, 20, 1)
        


class ScrollingText:
    def __init__(self, text, first_frame_length_count, length_of_screen, empty_buffer_length, refresh_period):
        self.extended_text = text + empty_buffer_length*" "

        self.first_frame_length_count = first_frame_length_count
        self.current_first_frames_counted = 0

        self.max_length_of_screen = length_of_screen
        self.tmp_display_string = self.extended_text

        self.last_updated_time = time.monotonic()
        self.refresh_period = refresh_period
        self.last_string = self.tmp_display_string[0:self.max_length_of_screen]
    def run_frame(self):
        if(time.monotonic()-self.last_updated_time > self.refresh_period):
            if(self.tmp_display_string==self.extended_text):
                if(self.current_first_frames_counted<self.first_frame_length_count):
                    #here, we want to pause for X number of frames at the start to give the user a chance to read it
                    self.current_first_frames_counted+=1
                    return self.tmp_display_string[0:self.max_length_of_screen]
                else:
                    #reset the frame counter here if we waited long enough
                    self.current_first_frames_counted=0
            #here, shuffle around the string to put the first character at the end of the cycle, iterate through circularly
            self.tmp_display_string=self.tmp_display_string[1:]+self.tmp_display_string[0]
            self.last_string = self.tmp_display_string[0:self.max_length_of_screen]
            return self.last_string
        else:
            return self.last_string



class Ride_Data:
    def __init__(self, ride_ID, is_ride_open, wait_time):
        try:
            self.display_name = master_ride_id_dict[ride_ID]
        except:
            self.display_name = str(ride_ID)
        self.ride_ID = ride_ID
        self.is_ride_open = is_ride_open
        self.current_wait_time = wait_time
        self.scrolling_title = RideTitle(self.display_name)
        self.RideData_display=RideData(self.is_ride_open, self.current_wait_time)
    def update_with_ride_data(self, is_ride_open, wait_time):
        self.is_ride_open = is_ride_open
        self.current_wait_time = wait_time
    def run_frame(self, display):
        self.scrolling_title.run_frame(display)
        self.RideData_display.run_frame(display)




class ParkData:
    def __init__(self, park_name, park_id):
        self.current_list_of_rides_dict = {}
        self.current_list_of_rides_dict_keys = []
        self.park_name = park_name
        self.park_id = park_id
    def update_data(self, list_of_ride_data):
        #input is a list of ride data in the following form
        #if its in the list, update data; if not, create a new one
        #[ride_id, is_open, wait_ime]
        for ride_data in list_of_ride_data:
            if(ride_data[0] not in self.current_list_of_rides_dict):
                tmp_ride_data = Ride_Data(ride_data[0], ride_data[1], ride_data[2])
                self.current_list_of_rides_dict[ride_data[0]] = tmp_ride_data
            else:
                self.current_list_of_rides_dict[ride_data[0]].update_with_ride_data(ride_data[1], ride_data[2])
        self.current_list_of_rides_dict_keys = list(self.current_list_of_rides_dict.keys())
    def get_ride_data_by_id(self, ride_id):
        return self.current_list_of_rides_dict[ride_id]

class ParkDataHandler:
    #maintain list of all parks
    #init init all park data
    
    #make a call to this to simply update data periodically
    #make a call to transition parks 
    #make a get current data call to display data on screen
    def __init__(self):
        #current park stored by ID
        self.main_MagicKingdomPark = ParkData("Magic Kingdom", MAGIC_KINGDOM_PARK_ID)
        self.current_park = MAGIC_KINGDOM_PARK_ID
        self.current_ride_shown_start_time = time.monotonic()
        self.current_ride_ptr = 0

    def _update_data(self, park, uart_ref):
        #park is an int for park ID
        if(park==MAGIC_KINGDOM_PARK_ID):
            passed = False
            while passed==False:
                uart_ref.write(MAGIC_KINGDOM_STR_CMD)
                tmp_data_string = ""
                data = uart_ref.read(1)
                while data is not None:
                    # convert bytearray to string
                    data_string = ''.join([chr(b) for b in data])
                    tmp_data_string = tmp_data_string + data_string
                    data = uart_ref.read(1)
                    #print(data)
                try:
                    #print("Data string: " + tmp_data_string + "\n")
                    list_of_mk_data_output = self._parse_data(tmp_data_string)
                    passed = True
                except:
                    #print("Failed.... retrying....")
                    pass
            self.main_MagicKingdomPark.update_data(list_of_mk_data_output)
            #serial send, wait, receive, return data struct
    def _parse_data(self, incoming_data_string):
        #string in the form of [ride_id, is_open, wait_time]
        master_ride_data_list = []
        new_string = incoming_data_string.split(' ')
        for inner_ride_list in new_string:
            tmp_string = inner_ride_list[1:len(inner_ride_list)-1]
            nums = tmp_string.split(',')
            ride_id = int(nums[0])
            is_open = bool(nums[1])
            wait_time = int(nums[2])
            tmp_ride_data = [ride_id, is_open, wait_time]
            master_ride_data_list.append(tmp_ride_data)
        return master_ride_data_list
    def global_park_update(self, uart_ref):
        #update current parks data; called from data handler
        self._update_data(self.current_park, uart_ref)
    def main_loop_call(self, main_display, button_pushed_should_iterate_bool):
        #return park ride; control auto-updating throughout list
        if(self.current_park==MAGIC_KINGDOM_PARK_ID):
            if(time.monotonic()-self.current_ride_shown_start_time > TIME_PER_RIDE or button_pushed_should_iterate_bool==True):
                #iterate to next ride; len for circular loop
                self.current_ride_shown_start_time = time.monotonic()
                self.current_ride_ptr = (self.current_ride_ptr+1)%len(self.main_MagicKingdomPark.current_list_of_rides_dict_keys)
            self.main_MagicKingdomPark.current_list_of_rides_dict[self.main_MagicKingdomPark.current_list_of_rides_dict_keys[self.current_ride_ptr]].run_frame(main_display)
        else:
            pass
        
class DisplayScreen:
    def __init__(self):
        self.i2c = busio.I2C(SCL, SDA)
        self.main_display = adafruit_ssd1306.SSD1306_I2C(128, 32, self.i2c)
        self.main_display.fill(0)
        self.main_display.show()
        pass
    def init_setup(self):
        self.main_display.fill(0)
        self.main_display.text("Loading Data...", 0, 0, 1)
        self.main_display.show()
    def text(self, a0, a1, a2, a3):
        self.main_display.text(a0, a1, a2, a3)
    def display_frame(self):
        self.main_display.show()
        self.main_display.fill(0)


class MainDataHandler:
    def __init__(self):
        self.main_ride_timer = time.monotonic()
        self.last_screen_updated_time = time.monotonic()

        self.last_updated_current_park_data_time = time.monotonic()

        self.main_uart = busio.UART(board.TX, board.RX, baudrate=9600)


        self.main_ParkDataHandler = ParkDataHandler()
        self.MainDisplayHandler = DisplayScreen()

        self.last_frame_button_value = 0

    def handle_button_push(self, button_value):
        if(button_value==1):
            if(self.last_frame_button_value!=button_value):
                self.last_frame_button_value = button_value
                return True
        self.last_frame_button_value = button_value
        return False
    def initial_setup(self):
        self.last_screen_updated_time = time.monotonic()
        self.MainDisplayHandler.text("Loading data....", 0, 0, 1)
        self.MainDisplayHandler.display_frame()
        self.main_ParkDataHandler.global_park_update(self.main_uart)
    def main_loop_call(self, input_switch_ride_button_value):
        ##First, check our timers and update our current page's data and displays accordingly

        should_update_to_next_ride = self.handle_button_push(input_switch_ride_button_value)
        if(time.monotonic()- self.last_updated_current_park_data_time > UPDATE_DATA_PERIOD):
            self.main_ParkDataHandler.global_park_update(self.main_uart)
            self.last_updated_current_park_data_time = time.monotonic()
        if(time.monotonic() - self.last_screen_updated_time > SCREEN_REFRESH_PERIOD):
            self.main_ParkDataHandler.main_loop_call(self.MainDisplayHandler, should_update_to_next_ride)
            self.MainDisplayHandler.display_frame()
            #self.last_screen_updated_time = time.monotonic()




