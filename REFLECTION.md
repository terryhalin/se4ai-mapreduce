# Reflection

Name: Htet Aung Lin (Terry)

Answer each question in 2–3 sentences.

**1. In Task 1, what did the shuffle do with the pairs your mapper produced? Why can the reducer only run once all mappers have finished?**

> The shuffle took all the (path, 1) pairs from the mappers and grouped them by path, so 33,665 pairs became 719 keys and each image got one list like [1, 1, 1]. The reducer has to wait until all mappers are done because any mapper could still send another pair for the same image. If we reduce too early, some counts would be too low.

**2. In Task 3, why did the original job give different answers with 1 and 4 workers? Why does moving the de-duplication into the reducer fix it, whatever the number of workers or partitions?**

> The mapper used a global set called already_sent, so the answer depended on which process ran which lines. It also only remembered the page and not the hour, so with 1 worker a page seen in hour 0 got dropped from later hours (hour 1 gave 48 instead of 129), and with 4 workers each process had its own set, so we got different wrong numbers (hour 8 was 9 with 1 worker and 87 with 4). When we move the de-duplication to the reducer with len(set(values)), the mapper has no memory anymore and the reducer always gets all the pages for one hour, so the answer is the same no matter how we split the work.

**3. The photo service from the lecture releases a new object-detection model and must re-tag 4 trillion stored photos. Which part of that job is the map step, is there a reduce step, and why would you run the computation on the machines that store the photos?**

> The map step is running the new model on each photo and outputting (photo_id, new tags). There isn't really a reduce step because each photo gets tagged on its own, at most we could add one to count tags or write the results back. We run it on the machines that store the photos because the model is way smaller than 4 trillion photos, so moving the model to the data is much faster and cheaper than sending all the photos over the network.
