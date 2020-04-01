import dominate
from dominate import document 
from dominate.tags import * 

class Documentation(object): 
    def __init__(self): 
        '''
        This function creates a dominate object, and adds text to the 
        documentation. In the end it creates an HTML file that 
        incldues the documentation. 
        ''' 
        self.doc = dominate.document(title="SafeChicago documentation")
        self.toc = {'1. Direction program' : ["1.0 Overview",
                                              "1.1 Input parameters", 
                                              "1.2 Expected output", 
                                              "1.3 Program limitations"],
                    '2. Heatmap program' : ["2.0 Overview", 
                                            "2.1 Starting out", 
                                            "2.2 Interpreting the map"],
                    '3. Safety score methodology' : ["3.0 Overview",
                                                     "3.1 Formula and\
                                                      justification", 
                                                     "3.2 Safety score\
                                                     threshold explained"]}
        self.toc_lvl1 = sorted(list(self.toc.keys()))
        self.back_to_toc = a("Back to Table of Contents", 
                              href='#Table of Contents')

        self.head() 
        self.table_of_contents() 
        self.section1_0()
        self.section1_1()
        self.section1_2()
        self.section1_3()
        self.section2_0()
        self.section2_1()
        self.section2_2()
        self.section3_0()
        self.section3_1()
        self.section3_2()
        
    def head(self): 
        '''
        Title and about section of the documentation. 
        '''
        with self.doc.head:
            self.doc += h1('Safe Chicago Documentation', 
                            style="color: #ff0000; background-color:#b3ddf2")

        self.doc += h2("About")
        self.doc += p('''Safe Chicago is a platform that aims to sensitize 
                     its users about crime in Chicago. This platform was 
                     developed by Kei Irizawa, Adam Oppenheimer, Swayam Sinha 
                     and Shyamsunder Sriram for our CS 122 project 
                     at the University of Chicago.''')

        self.doc += p('''Special thanks to Dr. Matthew Wachs for his 
                      invaluable guidance throughout our project.''')


    def table_of_contents(self): 
        '''
        Sets up table of contents lists, and creates text jump from 
        section to section using HTML tags.  
        '''
        self.doc += a(h2("Table of Contents"), id="Table of Contents")
        with self.doc: 
            with div(id='Table of Contents').add(ul()):
                for sec in self.toc_lvl1:
                    li(sec.title())
                    #li(a(sec.title(), href='#%s' % sec,))
                    with span(id=sec).add(ul()): 
                        for subsec in self.toc[sec]: 
                            li(a(subsec.title(), href='#%s' % subsec,))

    def section1_0(self): 
        '''
        Content for Section 1.0 
        '''
        self.doc += h2(self.toc_lvl1[0], id=self.toc_lvl1[0])
        self.doc += h3(self.toc[self.toc_lvl1[0]][0], 
                       id=self.toc[self.toc_lvl1[0]][0])
        self.doc += h4("Screenshot of our direction program interface")
        self.doc += img(src="1.0.png", alt="screenshot of program", 
                   style="width:900px;height:600px;")
        self.doc += p('\n')
        self.doc += self.back_to_toc

    def section1_1(self): 
        '''
        Content for Section 1.1
        '''
        self.doc += h3(self.toc[self.toc_lvl1[0]][1], 
                       id=self.toc[self.toc_lvl1[0]][1])
        self.doc += img(src="1.1.1.png", alt="pictures of input parameters", 
                   style="width:400px;height:200px;")
        self.doc += p('''Point of Departure (textbox): Can input full 
                    valid address or building name''')
        self.doc += p("Destination (textbox): Same as point of departure") 
        self.doc += p('''Community area (drop down menu): Select relevant 
                      community area. You have to select the right community
                      area of Chicago in order to walk. For instance if you 
                      enter Point of departure and Destination addresses meant
                      for Hyde Park, you need to select Hyde Park for the 
                      program to work, otherwise it will yield an error 
                      message. Refer to Error message in section 1.2 for 
                      more information''') 
        self.doc += p(''' Safety Score (drop down menu): This applies the 
                      safety score algorithm of our program. (Confused about 
                      safety scores? Check out Section 3 for a detailed 
                      description of our methodology in determining safety
                      scores.) There are three main safety score options:''')
        self.doc += p('''  i. Default: No safety score weighting.
                           Uses standard google maps output.''')
        self.doc += p('''  ii. Safer: Limited safety score weighting. 
                           Less priority given to streets with history of 
                           more severe crimes that has serious risk of 
                           causing harm to a potential passerby.''') 
        self.doc += p('''  iii. Safest: High safety score weighting. 
                          Less priority given to streets with history 
                          of crimes that have  moderate risk or above of
                          causing harm to a potential passerby.''')

        self.doc += self.back_to_toc

    def section1_2(self): 
        '''
        Content for Section 1.2
        '''
        self.doc += h3(self.toc[self.toc_lvl1[0]][2], 
                       id=self.toc[self.toc_lvl1[0]][2])
        self.doc += h4("Direction output")
        self.doc += p('''There will be a list of directions in the 
                         left side in a box. In case the page runs out of 
                         space for the directions, either scroll down or 
                         zoom out.''') 
        self.doc += img(src="1.2.1.png", alt="route box screenshot", 
                   style="width:200px;height:250px;")
        self.doc += h4("Map output")
        self.doc += p('''If the user inputs valid parameters, the there 
                    will be a map that will graphically displays the route 
                    shown above. ''')
        self.doc += img(src="1.2.2.png", alt="map directions screenshot", 
                   style="width:600px;height:300px;")
        self.doc += h4("Error message")
        self.doc += p('''In case of an invalid input, the program will 
                      return an error message. Note both the starting 
                      location and destination have to be in the same 
                      community area (refer to Section 1.3 for 
                      more details). ''') 
        self.doc += img(src="1.2.3.png", alt="error message screenshot", 
                   style="width:400px;height:200px;")
        self.doc += h4("Difference in output")
        self.doc += p('''Note sometimes the directions may or may not 
                     change based on safety score. Our safety score 
                     algorithm gives a score on how safe the street is, 
                     and there are three possible safety thresholds 
                     given an area. If there is no difference in route
                     between the 'default' and the 'safest' setting for 
                     example, this indicates that it is a safer area.
                     However, if there is a difference then note that 
                     the default route takes you through areas that 
                     have had dangerous crime since 2017.''')
        self.doc += self.back_to_toc

    def section1_3(self): 
        '''
        Content for Section 1.3
        '''
        self.doc += h3(self.toc[self.toc_lvl1[0]][3], 
                      id=self.toc[self.toc_lvl1[0]][3])
        self.doc += p('''This section is meant for addressing valid
                      inputs that may yield absurd results. That’s on us…
                      not on you. ''') 
        self.doc += h4('''Restricted search of starting point and destination 
                  within same community area''')
        self.doc += p('''You can only find destinations within a specific
                      community area. We intended to generalize our 
                      program to find the route between any two Chicago 
                      addresses. Unfortunately we could not figure out how
                      to deal with the streets on the boundary of two 
                      communities in our analysis. Thus we had to make 
                      the community area as a parameter of our program. If
                      you have figured this out please let us know! Besides,
                      most people walk within a community anyways so this
                     covers most of the cases. But if you’re still insistent
                     in using our program for covering borderline community
                     areas, the route directs you to or from a point that
                     is at the very edge of the community rather than the 
                     entire route''') 
        self.doc += h4('''Does not take into consideration of university 
                          campus police perimeters''')
        self.doc += p('''Addresses that require routes that pass through 
                        UChicago campus boundaries can yield strange 
                        outputs. This is because we used historical crime
                        data from the Chicago data portal. To get the 
                        actual route at UChicago (or any Chicago college 
                        campus for that matter), we would have needed 
                        the streets where university police/security 
                        is present and we would have had to hardcode that 
                        data in. This program should be used if you 
                        are venturing off campus, but remember that 
                        on campus you are safe within university
                        campus boundaries even if the program says if 
                        it is unsafe.''')
        self.doc += self.back_to_toc

    def section2_0(self): 
        '''
        Content for Section 2.0 
        '''
        self.doc += h2(self.toc_lvl1[1], id=self.toc_lvl1[1])
        self.doc += h3(self.toc[self.toc_lvl1[1]][0], 
                       id=self.toc[self.toc_lvl1[1]][0])
        self.doc += h4("Screenshot of our heatmap program interface.")
        self.doc += img(src="2.0.0.png", alt="screenshot of heatmap program", 
                   style="width:600px;height:300px;")
        self.doc += p('\n')
        self.doc += img(src="2.0.1.png", alt="zoom in out heatmap", 
                   style="width:400px;height:100px;")
        self.doc += p('\n')
        self.doc += self.back_to_toc
   

    def section2_1(self):
        '''
        Content for Section 2.1
        '''
        self.doc += h3(self.toc[self.toc_lvl1[1]][1], 
                       id=self.toc[self.toc_lvl1[1]][1])
        self.doc += img(src="2.1.1.png", alt="heatmap landing page", 
                   style="width:750px;height:400px;")
        self.doc += p('''This is what the map looks when you land on 
                         the page. The heatmap is organized in a rainbow 
                         color fashion, such that more red the heatmap is 
                         the more dangerous it is. Yes, the entire Chicago
                        is red, which is not that accurate. You need to 
                        zoom in for more accurate information. (Refer to 
                        section 2.2 for a picture of the different 
                       types of useful heatmaps''')
        self.doc += img(src="2.1.2.png", alt="top right hand corner button", 
                        style="width:600px;height:300px;")
        self.doc += p('''If you click the button on the top right
                         hand side, you will get a popup 
                         that resembles the picture above''') 
        self.doc += img(src="2.1.3.png", alt="blue icon statistics", 
                        style="width:300px;height:150px;") 
        self.doc += p('''Clicking on the blue icon will generate a popup 
                         that includes 4 graphs of statistics that the 
                         user can scroll down.''')
        self.doc += img(src="2.1.4.png", alt="most unsafe area by community", 
                        style="width:200px;height:150px;") 
        self.doc += p('''Clicking on the black circle will give the safety
                      score of the most unsafe area in that community. 
                      The higher the safety score, the more dangerous 
                      the area. There is no scale for these safety scores 
                      but you can compare the safety scores of the
                      different community areas.''') 
    def section2_2(self): 
        '''
        Content for Section 2.2
        '''
        self.doc += h3(self.toc[self.toc_lvl1[1]][2], 
                       id=self.toc[self.toc_lvl1[1]][2])
        self.doc += p(''' Notice how the heatmap is made of circles. 
                      These circles indicate a crime. The individual 
                      circles are clearer in the street level, and they get 
                      distorted at the community level creating a heatmap''') 
        self.doc += p('''We used the same crime weights for the safety score
                         and the heat map. Essentially, the crimes that we
                        thought would provide greater risk to the passerby 
                        should have a greater weight attached. Note that we 
                        did not use any fancy study to come up with these
                        values, but rather our intuition. This is a major
                        assumption that goes behind generating the
                        heatmap and the safety scores for that matter. We
                        have provided the weights for each type of crime
                        that we used below. Note that the higher the 
                        number, the more dangerous the crime. We used a
                        python dictionary to represent this information 
                        and use it in our safety score calulations (Refer
                        to Section 3 for more information).''')
        self.doc += img(src="2.2.1.png", alt="crime weights", 
                   style="width:600px;height:200px;")
        self.doc += p('\n')
        self.doc += self.back_to_toc

    def section3_0(self): 
        '''
        Content for Section 3.0 
        '''
        self.doc += h2(self.toc_lvl1[2], id=self.toc_lvl1[2])
        self.doc += h3(self.toc[self.toc_lvl1[2]][0], 
                       id=self.toc[self.toc_lvl1[2]][0])
        self.doc += p('''We can think of the Chicago street network as 
                      one big graph with nodes and edges. We assigned 
                      different crime weights for all the crimes as shown
                      in section 2.2. We then assigned each crime's
                      location to the nearest node. Now each node has a 
                      corresponding weight of crimes and probability 
                      of crimes happening near that area. This gave us an 
                      idea of creating a "safety score" that would give the
                      user an indication of how safe each node is.''' )
        self.doc += self.back_to_toc

    def section3_1(self): 
        '''
        Content for Section 3.1
        '''
        self.doc += h3(self.toc[self.toc_lvl1[2]][1], 
                       id=self.toc[self.toc_lvl1[2]][1])
        self.doc += img(src="3.1.1.png", alt="safety score formula", 
                       style="width:800px;height:400px;")
        self.doc += p('''We concluded that time of day, season and weather
                    (temperature) also affected the proability of crime
                    in addition to crime weights.''') 
        self.doc += h4('Time of day')
        self.doc += img(src="3.1.2.png", alt="time of day", 
                    style="width:800px;height:500px;")
        self.doc += p('''We used pyplot to figure out the total 
                      number of crimes for each time of day in Chicago 
                      since 2017. We concluded that during early morning
                      hours, there is a clear decrease in crimes. 
                      It is clear that time of day affects the crimes.''')
        self.doc += h4('Season')
        self.doc += img(src="3.1.3.png", alt="Season", 
                    style="width:800px;height:500px;")
        self.doc += p('''Season also affects the number of crimes. There 
                      is an increase in crime in the summer months. Also 
                      note that online research suggests that police
                      departments tend to report some December crimes
                      in January so that the can decrease number of crimes
                      that year for incentives. Online research suggests
                      this.''') 
        self.doc += h4('Safety score adjustment with profile weights')
        self.doc += p('''Even though the graphs suggest that there is a drop
                         of crimes in the early morning and increase in
                        crimes in the summer, making that general assumption
                        in our overall safety score formula would not be
                        that accurate because crime still exists in the
                        other months. Also it may not be the case that
                        all types of crimes are more probable in the
                        summer. Furthermore, in some community areas,
                        there are more actually more crimes in the winter!
                        Therefore we wanted to determine the probability
                        of certain crimes happening a little more 
                        abstractly. We weighed historical crimes that had
                        the same season and time of day bucket more 
                        than others, and crimes with different seasons
                        and times less. Because we are using historical 
                        data we are able to extract trends that are more
                        accurate than the general trends that we determined
                        from our simple pyplot graph.''') 
        self.doc += h4('Weather weights') 
        self.doc += img(src="3.1.4.png", alt="weather weights", 
                   style="width:800px;height:500px;")
        self.doc += p('''Graph above displays the total number of 
                         crimes by temperature in Fahrenheit. 
                    Source: http://crime.static-eric.com/''')
        self.doc += p('''It is true that season is closely correlated with 
                         weather, but it does not account for the drop of 
                         crimes in extreme temperatures. This is why we 
                         included the weather weight. However, the same 
                         logic for the "profile weight" for season and 
                         time of day can be applied here to improve the 
                          accuracy of our algorithm. However, this requires 
                          historical data to gain trends, and getting 
                          historical data for Chicago weather was 
                          cumbsersome. However, this could be a possible 
                          extension of our project.''') 
        self.doc += h4('''Time decay''')
        self.doc += img(src="3.1.5.png", alt="weather weights", 
                   style="width:400px;height:200px;")
        self.doc += p('''We wanted to give a greater weightage to more 
                         recent crime in an area, and since our stored 
                         crime dataset is updated with new crime, we want 
                         to give the older crimes less importance. 
                         Therefore we used a decay function that weighs 
                         crimes that were a year ago by half as much,
                        and crimes two years ago by a quarter as much
                         as indicated by our decay function''') 

    def section3_2(self): 
        '''
        Content for Section 3.2
        '''
        self.doc += h3(self.toc[self.toc_lvl1[2]][2], 
                       id=self.toc[self.toc_lvl1[2]][2])
        self.doc += img(src="3.2.1.png", alt="threshold explanation", 
                   style="width:800px;height:500px;")
        self.doc += p('''When using the direction program, different users
                         may be willing to take varying amounts of risks
                          when walking from Point A to Point B, and may
                          prioritize the shortest route here. Since we used 
                          Dijkstra's algorithm for determining the shortest
                          route, we wanted to adjust the lengths of the 
                          routes between each node according to the safety
                          threshold. We distributed all the crimes based on
                        safety scores and increased the lengths of all 
                        streets attached to the node which has a relatively
                        high percentile based on the corresponding safety 
                        threshold. Furthermore, users sometimes maybe in a 
                        situation where they have to pick between two 
                        dangerous streets, and we wanted to give them the 
                        option to pick the safer route in this scenario.''') 
        self.doc += p('''Default just calculated the shortest path 
                        without modifying the lengths of the streets''')
        self.doc += p('''Safer increased the street lengths by 10x for nodes 
                         between the 75th and 90th percentile, and 20x 
                          for nodes above the 90th percentile.''')
        self.doc += p('''Safest increased the street lengths by 10x for nodes
                         between the 25th and 75th percentile, 20x for nodes 
                         between the 75th and 90th percentile, and 40x 
                         for nodes above the 90th percentile.''')
        self.doc += self.back_to_toc

def construct_doc(): 
    '''
    Converts dominate object in our Documentation class into an HTML file. 
    '''
    full_doc = Documentation()
    with open('safe.html', 'w') as f:
        f.write(full_doc.doc.render())

if __name__ == "__main__":
    construct_doc()
