def obstacle():
        '''
        The map is 2D array. The ranges are [0;20] and [-20;-20] horizontally
        and [20;-20], [0;-20] vertically.
        If the head of the snake (self.snake[0:0]) colides with any of the border, Game ends.
        '''
        obstacles = []
        for i in range(0, 21):
            point = []
            point.append(0)
            point.append(i)
            obstacles.append(point)
                    
            
        for l in range(0,21):
            point = []
            point.append(l)
            point.append(0)
            obstacles.append(point)

        print (obstacles)
       

if __name__ == "__main__":
    print (obstacle())
    
