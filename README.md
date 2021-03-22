# FuzzyLogic
1. Requirements:
    * Create 3x3 inputs
    * Create 1x3 outputs
2. Data compuer re-sell
    * Input data:
      * Price[50-1000] - Whereas cheap is [50-400], Middle - [350-750] and Expensive [650-1000]
      * Speed[1-10] - Where Slow [1-5], Average - [4-8] and Fast [7-8]
      * Year of build[2014-2021] - Where Old is [2014-2018], Used - [2015-2020] and Almost new [2017-2071]
      ![alt text](https://i.ibb.co/42RvwTJ/fuzzy.png)<br>
    * Output data:
      * probability of success in percentage to sell compuer. Where Low is 0-40%, Average - 30-70% and High - 65-100% 
      ![alt text](https://i.ibb.co/FbbJwsW/fuzzy.png)<br>
3. Rules<br>
  ![alt text](https://i.ibb.co/sHCXNpC/image.png)<br>
4. Test 
    * Input
      * Price: 250
      * Speed: 8
      * Year of Build: 2019
    * Outputs:
      * COA method: ~82%
      * MOM mothod: 85%<br>
      ![alt text](https://i.ibb.co/fYRvTqk/image.png)<br>
