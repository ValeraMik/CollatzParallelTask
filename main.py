import threading
import queue
import time

def collatz_steps(n):
    """
    Обчислення кількості кроків для виродження числа n до 1 за гіпотезою Колаца.
    """
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def worker(task_queue, result_queue):
    """
    Потік-працівник: обчислює кількість кроків для чисел з черги завдань 
    та додає результат у чергу результатів.
    """
    while not task_queue.empty():
        try:
            number = task_queue.get_nowait()
        except queue.Empty:
            break
        steps = collatz_steps(number)
        result_queue.put(steps)
        task_queue.task_done()

def main():
    # Параметри
    total_numbers = 10_000_000  # Загальна кількість чисел
    num_threads = 8             # Кількість потоків (можна змінити вручну)

    # Черги завдань і результатів
    task_queue = queue.Queue()
    result_queue = queue.Queue()

    # Додавання завдань у чергу
    for i in range(1, total_numbers + 1):
        task_queue.put(i)

    # Створення та запуск потоків
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(task_queue, result_queue))
        thread.start()
        threads.append(thread)

    # Очікування завершення всіх потоків
    for thread in threads:
        thread.join()

    # Обчислення середньої кількості кроків
    total_steps = 0
    processed_numbers = 0
    while not result_queue.empty():
        total_steps += result_queue.get()
        processed_numbers += 1

    average_steps = total_steps / processed_numbers
    print(f"Середня кількість кроків: {average_steps}")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Час виконання: {end_time - start_time:.2f} секунд")
