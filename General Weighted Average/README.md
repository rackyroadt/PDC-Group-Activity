1. Which approach demonstrates true parallelism in Python? Explain.

```- Multiprocessing demonstrates true parallelism in Python. This is because each process runs in its own separate memory space and uses its own Python interpreter, allowing it to fully utilize multiple CPU cores. In contrast, multithreading in CPython is limited by the Global Interpreter Lock (GIL), which allows only one thread to execute Python bytecode at a time. Therefore, only multiprocessing can truly execute tasks simultaneously on multiple cores. ```

2. Compare execution times between multithreading and multiprocessing.

``` - In this program, multithreading is usually slightly faster than multiprocessing for a small number of subjects. This is because creating threads has less overhead compared to creating separate processes, which require more memory and system resources. However, the time difference is usually small since the task (sleep + simple append) is lightweight. For simple operations like this, threading often completes faster due to lower startup cost. ```

3. Can Python handle true parallelism using threads? Why or why not?

4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why?

5. Which method is better for CPU-bound tasks and which for I/O-bound tasks?

6. How did your group apply creative coding or algorithmic solutions in this glab?