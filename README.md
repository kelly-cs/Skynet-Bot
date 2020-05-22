# Skynet-Bot
A self learning AI bot for generic applications. 

This was created using base code for creating neural networks, and has been updated to perform actions on a client and train a model entirely over a web API. Ideally, this is intended to be used so that a model can be trained given input from any generic application, given a list of:
 - Possible Actions
 - The Current Game State

from the application. The neural network responds in kind with an appropriate action to take, given the list of possible actions and the current game state. The application is intended to apply the action itself, in order to limit the scope of the neural network's role.

This has only been adapted to use an open-source Snake title at this time, but was intended to be upgraded to utilize more complex games using the same action list / game state formula. In lieu of more comprehensive and powerful neural networks, like Alphastar, this has been shelved for now. It may be updated for a niche use in the future.

