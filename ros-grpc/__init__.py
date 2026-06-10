async def fetch_data(): #why async is here
    # Simulate an asynchronous operation, such as fetching data from a database or an API
    await asyncio.sleep(1)  # Simulating a delay
    return "Data fetched successfully"  #can we use it without async and await
# Example usage
import asyncio      