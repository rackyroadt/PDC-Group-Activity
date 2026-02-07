1. Which approach demonstrates true parallelism in Python? Explain.

```Multiprocessing demonstrates true parallelism in Python. This is because each process runs in its own separate memory space and uses its own Python interpreter, allowing it to fully utilize multiple CPU cores. In contrast, multithreading in CPython is limited by the Global Interpreter Lock (GIL), which allows only one thread to execute Python bytecode at a time. Therefore, only multiprocessing can truly execute tasks simultaneously on multiple cores.```

2. Compare execution times between multithreading and multiprocessing.

```In this program, multithreading is usually slightly faster than multiprocessing for a small number of subjects. This is because creating threads has less overhead compared to creating separate processes, which require more memory and system resources. However, the time difference is usually small since the task (sleep + simple append) is lightweight. For simple operations like this, threading often completes faster due to lower startup cost.```

3. Can Python handle true parallelism using threads? Why or why not?

```In standard CPython, Python cannot achieve true parallelism using threads for CPU-bound tasks because of the Global Interpreter Lock (GIL). The GIL ensures that only one thread executes Python bytecode at a time, even on multi-core systems. This means threads run concurrently but not truly in parallel for CPU-heavy work. However, threads can still be effective for I/O-bound operations.```

4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why?

```If we input 1000 grades, both methods will create 1000 threads or processes. In this case, multiprocessing may become slower due to high overhead from creating many processes and managing inter-process communication using a Queue. Multithreading may perform better for this lightweight task because thread creation is cheaper than process creation. However, if the computation per grade was CPU-intensive, multiprocessing would likely outperform threading by utilizing multiple cores.```

5. Which method is better for CPU-bound tasks and which for I/O-bound tasks?

<<<<<<< HEAD
6. How did your group apply creative coding or algorithmic solutions in this glab?
=======
```Multiprocessing is better for CPU-bound tasks because it bypasses the GIL and uses multiple CPU cores, allowing real parallel execution. Multithreading is better for I/O-bound tasks (such as file reading, network requests, or waiting operations) because while one thread waits for I/O, other threads can continue running. In this program, since the task is lightweight and includes time.sleep() (which simulates waiting), multithreading performs efficiently.```

6. How did your group apply creative coding or algorithmic solutions in this lab?

```In this lab, we applied creative coding by designing a comparative system that measures and analyzes the performance difference between multithreading and multiprocessing. Instead of just computing the GWA, we implemented timing analysis, structured result storage, and a formatted performance comparison table. We also handled synchronization using locks and safe communication using a queue to avoid race conditions. This allowed us to combine algorithmic thinking with system-level programming concepts to clearly demonstrate how concurrency works in Python.```
>>>>>>> 19a268d5894fe32798c32def9603162d34db704b
