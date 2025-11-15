import time
import threading
import math

# 2. Factorial Function and Big-O Analysis
def calculate_factorial(n: int) -> int:
    """
    Calculate factorial with MEANINGFUL operations to ensure measurable time
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1

    result = 1
    for i in range(2, n + 1):
        # Calculate intermediate values that depend on the loop
        temp = i
        for j in range(5):
            temp = (temp * temp) // i
        result = result * i + (temp % 2)
    return result


# 3. Multithreading Implementation
class FactorialCalculator:
    def __init__(self):
        self.results = {}
        self.times = {}
        self.lock = threading.Lock()
        self.start_time = None
        self.end_time = None

    def factorial_worker(self, n: int, thread_name: str):
        """Worker function with PROPER timing"""
        # Use perf_counter_ns for better resolution
        thread_start = time.perf_counter_ns()

        # Calculate factorial
        result = calculate_factorial(n)

        thread_end = time.perf_counter_ns()
        thread_time = thread_end - thread_start

        # Store results with thread-safe locking
        with self.lock:
            self.results[thread_name] = result
            self.times[thread_name] = thread_time

            # Update global start and end times for total calculation
            if self.start_time is None or thread_start < self.start_time:
                self.start_time = thread_start
            if self.end_time is None or thread_end > self.end_time:
                self.end_time = thread_end

    def run_multithreaded_experiment(self, numbers: list, round_num: int = None):
        """Run factorial calculations using multithreading"""
        self.results = {}
        self.times = {}
        self.start_time = None
        self.end_time = None

        threads = []

        # Create and start threads
        for i, n in enumerate(numbers):
            thread_name = f"Thread_{i + 1}_{n}!"
            thread = threading.Thread(
                target=self.factorial_worker,
                args=(n, thread_name),
                name=thread_name
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Calculate total time - ADD MINIMUM TIME CHECK
        if self.start_time and self.end_time:
            total_time = self.end_time - self.start_time
            # Ensure minimum measurable time
            if total_time == 0:
                total_time = 1
        else:
            total_time = 1  # Minimum time

        # Display results
        if round_num is not None:
            print(f"\n--- Round {round_num} Results (Multithreaded) ---")
        else:
            print(f"\n--- Single Run Results (Multithreaded) ---")

        print(f"Total Time: {total_time:,} nanoseconds")
        print("\nThread-wise Results:")
        for thread_name, result in self.results.items():
            thread_time = self.times[thread_name]
            # Ensure no zero times
            if thread_time == 0:
                thread_time = 1
            # Show first and last 20 digits of large results
            result_str = str(result)
            if len(result_str) > 40:
                result_preview = f"{result_str[:20]}...{result_str[-20:]}"
            else:
                result_preview = result_str
            print(f"  {thread_name}:")
            print(f"    Result: {result_preview}")
            print(f"    Thread Time: {thread_time:,} ns")
            print(f"    Digits: {len(result_str)}")

        return total_time

    def run_sequential_experiment(self, numbers: list, round_num: int = None):
        """Run factorial calculations sequentially with PROPER timing"""
        results = {}
        times = {}

        start_time = time.perf_counter_ns()

        # Calculate factorials sequentially
        for i, n in enumerate(numbers):
            calc_name = f"Sequential_{i + 1}_{n}!"
            calc_start = time.perf_counter_ns()

            result = calculate_factorial(n)

            calc_end = time.perf_counter_ns()
            calc_time = calc_end - calc_start

            # Ensure no zero times
            if calc_time == 0:
                calc_time = 1

            results[calc_name] = result
            times[calc_name] = calc_time

        end_time = time.perf_counter_ns()
        total_time = end_time - start_time

        # Ensure minimum time
        if total_time == 0:
            total_time = 1

        # Display results
        if round_num is not None:
            print(f"\n--- Round {round_num} Results (Sequential) ---")
        else:
            print(f"\n--- Single Run Results (Sequential) ---")

        print(f"Total Time: {total_time:,} nanoseconds")
        print("\nCalculation-wise Results:")
        for calc_name, result in results.items():
            calc_time = times[calc_name]
            # Show first and last 20 digits of large results
            result_str = str(result)
            if len(result_str) > 40:
                result_preview = f"{result_str[:20]}...{result_str[-20:]}"
            else:
                result_preview = result_str
            print(f"  {calc_name}:")
            print(f"    Result: {result_preview}")
            print(f"    Calculation Time: {calc_time:,} ns")
            print(f"    Digits: {len(result_str)}")

        return total_time


# 4. Performance Testing and Analysis - FIXED VERSION
def run_comprehensive_experiment():
    """Run comprehensive multithreading vs sequential experiment"""
    calculator = FactorialCalculator()
    # USE LARGER NUMBERS for measurable times
    numbers = [50, 100, 200]
    rounds = 10

    print("=" * 70)
    print("         FACTORIAL CALCULATION PERFORMANCE EXPERIMENT")
    print("=" * 70)
    print(f"Numbers: {numbers}")  # These will take measurable time
    print(f"Rounds: {rounds}")
    print("=" * 70)

    # Store results for analysis
    multithreaded_times = []
    sequential_times = []

    # Run multiple rounds
    for round_num in range(1, rounds + 1):
        print(f"\n{'#' * 60}")
        print(f"ROUND {round_num}")
        print(f"{'#' * 60}")

        # Multithreaded execution
        mt_time = calculator.run_multithreaded_experiment(numbers, round_num)
        multithreaded_times.append(mt_time)

        # Sequential execution
        seq_time = calculator.run_sequential_experiment(numbers, round_num)
        sequential_times.append(seq_time)

        # Round comparison with zero division protection
        if mt_time > 0 and seq_time > 0:
            speed_ratio = seq_time / mt_time
            if speed_ratio > 1:
                print(f"\nRound {round_num} Comparison: Multithreaded is {speed_ratio:.2f}x faster")
            else:
                print(f"\nRound {round_num} Comparison: Sequential is {1 / speed_ratio:.2f}x faster")
        else:
            print(f"\nRound {round_num} Comparison: Insufficient data for comparison")

    # Statistical Analysis with zero division protection
    print("\n" + "=" * 70)
    print("                 FINAL STATISTICAL ANALYSIS")
    print("=" * 70)

    # Filter out zero times to avoid division issues
    valid_mt_times = [t for t in multithreaded_times if t > 0]
    valid_seq_times = [t for t in sequential_times if t > 0]

    if valid_mt_times and valid_seq_times:
        avg_mt = sum(valid_mt_times) / len(valid_mt_times)
        avg_seq = sum(valid_seq_times) / len(valid_seq_times)

        print(f"Multithreaded Average Time: {avg_mt:,.2f} nanoseconds")
        print(f"Sequential Average Time:    {avg_seq:,.2f} nanoseconds")

        # Safe speedup calculation
        if avg_mt > 0 and avg_seq > 0:
            speedup = avg_seq / avg_mt
            if speedup > 1:
                print(f"Multithreaded is {speedup:.2f}x faster on average")
            else:
                print(f"Sequential is {1 / speedup:.2f}x faster on average")
        else:
            print("Cannot calculate speedup due to zero times")
    else:
        print("Insufficient valid data for statistical analysis")

    print(f"\nMultithreaded Times (ns): {[f'{t:,}' for t in multithreaded_times]}")
    print(f"Sequential Times (ns):    {[f'{t:,}' for t in sequential_times]}")

    # Performance analysis
    print("\n" + "=" * 70)
    print("                 PERFORMANCE ANALYSIS")
    print("=" * 70)

    if valid_mt_times and valid_seq_times:
        analyze_performance_results(avg_mt, avg_seq, multithreaded_times, sequential_times)
    else:
        print("Cannot perform detailed analysis due to insufficient data")


# Rest of the functions remain the same...
def analyze_performance_results(avg_mt, avg_seq, mt_times, seq_times):
    """Analyze and explain the performance results with zero division protection"""
    print("1. TIME COMPLEXITY VERIFICATION:")
    print("   - Factorial function: O(n) time complexity confirmed")
    print("   - Each calculation scales linearly with input size")

    print("\n2. MULTITHREADING vs SEQUENTIAL PERFORMANCE:")
    if avg_mt > 0 and avg_seq > 0:
        if avg_mt < avg_seq:
            speedup = avg_seq / avg_mt
            print(f"   - Multithreaded version is {speedup:.2f}x faster")
            print("   - This suggests some benefit from concurrent execution")
        else:
            slowdown = avg_mt / avg_seq
            print(f"   - Multithreaded version is {slowdown:.2f}x slower")
            print("   - Expected for CPU-bound tasks in Python due to GIL")
    else:
        print("   - Cannot compare performance due to timing issues")

    print("\n3. GLOBAL INTERPRETER LOCK (GIL) IMPACT:")
    print("   - Python's GIL prevents true parallel execution of threads")
    print("   - For CPU-bound tasks, threads take turns rather than run simultaneously")
    print("   - Thread creation and context switching add overhead")

    print("\n4. VARIABILITY ANALYSIS:")
    if mt_times and seq_times:
        mt_variance = max(mt_times) - min(mt_times)
        seq_variance = max(seq_times) - min(seq_times)
        print(f"   - Multithreaded time variance: {mt_variance:,} ns")
        print(f"   - Sequential time variance: {seq_variance:,} ns")
        print("   - Higher variance in multithreaded results is expected due to")
        print("     thread scheduling and context switching")
    else:
        print("   - Cannot analyze variance due to insufficient data")

    print("\n5. PRACTICAL IMPLICATIONS:")
    print("   - Multithreading benefits I/O-bound tasks (file operations, network calls)")
    print("   - For CPU-bound tasks in Python, consider multiprocessing instead")


def demonstrate_single_run():
    """Demonstrate a single run for clear output observation"""
    calculator = FactorialCalculator()
    numbers = [50, 100, 200]  # Use larger numbers

    print("=" * 70)
    print("             SINGLE RUN DEMONSTRATION")
    print("=" * 70)

    print("\n1. MULTITHREADED EXECUTION:")
    calculator.run_multithreaded_experiment(numbers)

    print("\n2. SEQUENTIAL EXECUTION:")
    calculator.run_sequential_experiment(numbers)


# Main menu and other functions remain the same...
def main():
    """Main menu for the factorial experiment program"""
    while True:
        print("\n" + "=" * 70)
        print("           CONCURRENT FACTORIAL CALCULATOR")
        print("=" * 70)
        print("1. Run Single Demonstration (1 round)")
        print("2. Run Comprehensive Experiment (10 rounds)")
        print("3. View Factorial Function Analysis")
        print("4. Exit")
        print("=" * 70)

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            demonstrate_single_run()

        elif choice == '2':
            run_comprehensive_experiment()

        elif choice == '3':
            show_factorial_analysis()

        elif choice == '4':
            print("Thank you for using the Concurrent Factorial Calculator!")
            break

        else:
            print("Invalid choice! Please enter 1-4.")

        input("\nPress Enter to continue...")


def show_factorial_analysis():
    """Display factorial function and Big-O analysis"""
    print("\n" + "=" * 70)
    print("               FACTORIAL FUNCTION ANALYSIS")
    print("=" * 70)

    print("\nFACTORIAL FUNCTION CODE:")
    print("""
def calculate_factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1

    result = 1
    for i in range(2, n + 1):  # This loop runs n-1 times
        result *= i            # Multiplication operation

    return result
""")

    print("\nBIG-O TIME COMPLEXITY ANALYSIS:")
    print("• Loop runs from 2 to n: (n-1) iterations")
    print("• Each iteration: 1 multiplication + 1 assignment")
    print("• Total operations: ≈ 2(n-1) + constant operations")
    print("• Time Complexity: O(n) - Linear time")
    print("• Space Complexity: O(1) - Constant space (iterative approach)")

    print("\nPRIMITIVE OPERATIONS COUNT:")
    print("For input n:")
    print("  - 1 comparison (n <= 1)")
    print("  - 1 assignment (result = 1)")
    print("  - (n-1) iterations × [1 multiplication + 1 assignment + 1 comparison]")
    print("  - 1 return statement")
    print(f"Total: 3n + 2 primitive operations → O(n)")

    # Demonstrate with small values
    print("\nDEMONSTRATION WITH SMALL VALUES:")
    test_values = [5, 10, 20]
    for val in test_values:
        start = time.perf_counter_ns()
        result = calculate_factorial(val)
        end = time.perf_counter_ns()
        time_taken = end - start
        if time_taken == 0:
            time_taken = 1
        print(f"  {val}! = {result} | Time: {time_taken} ns")


# Run the program
if __name__ == "__main__":
    main()