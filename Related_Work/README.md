* This folder explores previous and current works in the AR field.
    * [1997, Azuma Ronald. A Survey of Augmented Reality](#takeaways-from-1997-azuma-ronald-a-survey-of-augmented-reality)
    * [2016, Azuma Ronald. The Most Important Challenge facing AR](#takeaways-from-2016-azuma-ronald-the-most-important-challenge-facing-AR)

## Takeaways from 1997, Azuma Ronald: [A Survey of Augmented Reality](https://www.cs.unc.edu/~azuma/ARpresence.pdf)
* *"While the CGI effects in movies interact with the real world (e.g. actors), the movie is not an interactive media [and thus not AR]."*
* *"AR is useful because it displays information that we can't directly detect with our own senses."*
* *"In addition to augmenting, can AR detract from reality, e.g. remove a desk from the field of vision by imposing an extrapolated background."*
* Presenting AR content had two paths: optical blending (the HoloLens took this route) and video blending (basically a VR headset with a video feed of the real world).
    * Optical blending has a narrower field of view, and requires optical expertise if the holograms are to be realistic.
    * Video blending has more computational overhead, resolution ceiling, an eye-offset and the user is effectively blind once power goes out.
* The Registration Problem:
    * It's a matter of alignment. *"If the virtual object is not where the real tumor is, the surgeon will miss the tumor."*
    * Identifying errors can be problematic due to visual capture, *the tendency of the brain to believe visual information and override all other senses*. Herein lies potential for optical illusions.
    * This becomes more pronounced when the user is moving around.
    * Possible suggested solutions were movement prediction, fiducials placed in predetermined patterns. The HoloLens requires the user to calibrate the device.
* The Sensing Problem:
    * Refers to tracking the user's head and the location of objects in the environment.
    * AR needs sensors that can read varied types of inputs, are accurate and have a long range. GPS was at best accurate to 1cm back then (but not in real time).
* What promising areas were anticipated in 1997? Hybrid approaches to design, real-time systems with guarantees on computation times, research on human perception, portable device, adding other displays like sound, and of course, societal attitudes, *e.g. is an AR device desirable?*
* Were outdoor tracking solved, Azuma believes a swarm of applications will become available, e.g. navigation aid (think Google Maps in your field of vision), visualizing how locations were in the past. The ultimate endgame is having surreal virtual objects in our physical world such that we can't tell the difference.  

* In 2016, Azuma did a reflection on his 1997 paper

## Takeaways from 2016, Azuma Ronald: [The Most Important Challenge Facing AR](http://www.ronaldazuma.com/papers/Presence_AR_challenge.pdf)
* In '97, AR contraptions were complex and expensive, thus for governments and companies. We've witnessed a shift towards AR for mass devices like tablets, smartphones, HoloLenses, etc.
* Problems that need to be solved:
    * Precise tracking in varied environments to pixel-accurate registration.
    * Wide field of view optical see-through near-eye displays that can selectively block light.
    * Keyboard-free and mouse-free user interfaces.
    * Semantic understanding of real world objects without predetermined infrastructure.
        * SLAM knows *where* the objects are, but not *what* the objects are.
* Solving semantic understanding is crucial in making AR a mass-adopted platform. We could develop robust computer vision, or piggyback existing data to model the real world beforehand.
* Approaches to making compelling AR media:
    * Reinforcing. Make inherently important locations even more poignant, e.g. [110 Stories](http://www.110stories.com/)
    * Reskinning. Reinterpret otherwise normal environments, e.g. [Belief Circles in Rainbows End](https://en.wikipedia.org/wiki/Rainbows_End#Belief_circles), virtual gyms in Pokémon GO.
    * Remembering. Setting virtual time machines for personally significant events, e.g. [The Holoportation Project](https://www.microsoft.com/en-us/research/project/holoportation-3/), recreating your child's first steps at the exact spot.
