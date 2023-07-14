# Defensive Zone Puck Battles and Breakout Success
<a name="br1"></a> 

Ethan Parliament

Queens University, Kingston ON, Canada

**1**

**Introduction**

Ice hockey is a sport that has embraced analytics to better understand the game and gain

a competitive edge. As such, this paper aims to delve into two important aspects of

hockey analytics: the importance of puck possession and winning battles in the defen-

sive zone, and the relationship between puck battles and successful breakouts, using

breakout success rates, expected goals (xg), and possession time. With a focus on un-

derstanding the factors that contribute to success in the defensive zone and successful

transitions to offense, this paper provides valuable insights for teams and analysts look-

ing to gain an edge in the modern game of hockey.

**2**

**Background Information**

Breaking out of the defensive zone is a critical aspect of hockey, as it sets up the team

for offensive opportunities while minimizing the risk of conceding a goal. Strong

breakouts can lead to quick counter-attacks and more sustained possession in the offen-

sive zone, resulting in increased scoring chances and ultimately, higher goal-scoring.

In contrast, poor breakouts can lead to turnovers in the defensive zone, putting the team

at a disadvantage and increasing the likelihood of conceding a goal. Therefore, under-

standing which puck battles lead to successful breakouts and how to effectively win

those battles is essential in improving a team's performance on both ends of the ice.

The quality of a breakout can be measured in a few ways. The simplest and most im-

portant way of evaluating breakout quality is whether or not the breakout succeeded.

This is measured by recording if the breaking out team successfully moves the puck out

of the defensive zone while maintaining possession of the puck. Another way to meas-

ure the quality of a breakout is through the use of expected goals (xg). By tracking

breakout attempts, we can score them based on the cumulative xg that they generate

during that possession. Finally, a third way we can evaluate a breakout is by tracking

time of possession. Time of possession can serve as a reliable indicator of which team

is in control, and thus can also provide valuable insight into the strength of a team's

breakout strategy.



<a name="br2"></a> 

**3**

**Algorithms and Methods**

**3.1**

**The Dataset**

The data provided for this competition by Sportlogiq included data from 20 games of

the 2020-21 SHL season. Each row represents a single event that occurred during the

game, and includes data such as the team and player, event name and type, success/fail-

ure, and the time and location of the event. The dataset also includes the xg for all shot

attempts. The most important features of the dataset for this research was the event

name, and the location of the event. Two key event names are ‘lpr’ (loose puck recov-

ery) and ‘controlledexit’. These events were crucial for the continuation of this re-

search.

**3.2**

**Method**

Before getting into the analysis, some pre-processing had to be done to put the data into

a form that was easier to work with for these purposes. Using an array of Pandas Data-

Frames, the dataset was broken up into individual possessions. Once each individual

possession was accessible, further analysis could be done.

Firstly, an analysis of loose puck recoveries (lpr) was conducted to get a general under-

standing of the problem and the dataset. Each possession that included an lpr event had

its location record as X and Y coordinates, as well as other pieces of information, such

as shots taken, cumulative xg, and total time of possession. These features that were

extracted from the dataset can now be plotted to visualize the impact that they have on

the game. This research only considered possessions that began in the defensive zone,

in order to get a deeper understanding of the success of breakouts.

After looking at lprs, different breakout strategies can be considered. Three different

metrics were used to evaluate the quality of a breakout. For each metric, the data was

grouped using a 2d histogram to capture the spatial data of each metric using the X and

Y coordinates recorded during the pre-processing phase. The first metric, breakout suc-

cess utilized a net breakout success rate. A successful breakout was given the score of

+1, and a failed breakout was given a -1. Each bin in the histogram records the net

number of successful breakout attempts.

The second metric considered when evaluating breakouts is the cumulative xg that

comes from the possession after the breakout. This was tracked using play sequencing

techniques to track shot attempts and their respective xg for each possession. Then each

possession is given a total xg equal to the sum of all xg during that possession.

The third and final metric used is time of possession. This metric followed a similar

approach to the first 2, using a 2d histogram to bin the data with respect to the starting

locations of the data. This time, the weights used for the bins of the histogram was the

time of possession, taken from the ‘compiledgametime’ field of the dataset.



<a name="br3"></a> 

3

**3.3**

**Visualizing the Data**

The locations used in the data and all plots shown are based on a grid centered at center

ice. The bounds of the defensive zone is shown below.

![image](https://github.com/eparly/Linhac2023/assets/105623247/a61c2352-1742-4d1d-9542-b0d6bc7cb305)

*Figure 1: The scale use for coordinates in the defensive zone*

The end boards are located along the Y = -100 line, and the blue line is located at the

Y = -25 line. All figures shown in this report work with respect to the coordinates

shown.

**4**

**Results**

**4.1**

**Breakout Success**

For the simple net breakout success metric, there is are a few clear locations to start the

breakout from. The most obvious are the two zones from the hashmarks to just before

the blueline; the closer you are to the neutral zone, the easier it is to get the puck out.

More interestingly are the other large zones directly behind the net and in the slot. These

zones also have a very high chance of a successful breakout after winning an lpr in

these locations.

![image](https://github.com/eparly/Linhac2023/assets/105623247/1be701c6-e6cc-4b6a-8ce4-54b5cba9780d)

*Figure 2: The locations of highest (red) and lowest (blue) breakout success*



<a name="br4"></a> 

**4.2**

**Expected Goals**

In the scenario when you are losing and need to score, maximizing your xg will lead to

your greatest chance of success. Compared to the breakout success metric above, max-

imizing your xg off of a breakout should come from different areas of the ice. Once

again, starting your breakout from behind the ice is a good idea, but winning lprs from

the high slot does not provide the same results as before. Instead, look to move the puck

and breakout from closer to the blueline in the center of the ice. This will provide your

team with a higher chance of scoring, but with a higher degree of difficulty and risk

associated with it.

![image](https://github.com/eparly/Linhac2023/assets/105623247/f914bb62-6698-40a7-9abe-b33ab5106540)

*Figure 3: The locations of the highest (red) and lowest (blue) xg based on starting location*

**4.3**

**Time of Possession**

In the case you want to play a strong puck possession game, breakouts along the boards

are your best bet. When looking at time of possession for breakout locations, along the

boards has a strong advantage compared to moving the puck through the middle of the

ice. Both expected goals and breakout success metrics consider the middle of the ice

strong areas to breakout through, but in terms of puck possession, the boards are a much

safer choice.

![image](https://github.com/eparly/Linhac2023/assets/105623247/efa8c03c-e0b4-4a96-acb5-796b89c893d4)

*Figure 4: The highest (red) and lowest (blue) time of possessions based on starting location*



<a name="br5"></a> 

5

**5**

**Summary of Results and Next Steps**

Like any game, hockey requires a changing strategy depending on what the current

game situation is. Using the results above, different defensive strategies can be used

depending on the situation. If you are currently in a winning situation and want to play

defensively, forcing the puck to behind the net and, and towards the hashmarks is the

most effective strategy, as well as keeping the puck away from the corners. However,

if you are losing and need to generate some offensive opportunities, allowing the puck

to enter the middle of the defensive zone can be a risky, but rewarding strategy that

allows your team to create high quality scoring opportunities from the defensive zone.

Finally, if you need to control the pace of play of the game and hold the puck as long

as possible, breaking out from along the boards can make your possessions last two to

three times longer on average.

Moving forward, there are several areas of research that could build upon this study's

findings. One potential avenue would be to incorporate additional variables into the

analysis, such as player position and handedness, to better understand how these factors

impact successful breakouts. Another possibility would be to compare breakout success

rates between different game situations, such as even strength versus power play sce-

narios. Additionally, this study could be expanded to include a larger sample size of

games to increase the statistical power and generalizability of the findings. Overall,

there is much potential for future research to build upon the insights gained from this

study and further advance our understanding of the importance of breaking out of the

defensive zone in hockey.

**6**

**Link to Code**

https://github.com/eparly/Linhac2023


