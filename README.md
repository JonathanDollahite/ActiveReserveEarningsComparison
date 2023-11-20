# Active vs Reserve Lifetime Earnings Comparison

## Overview
This Dash web application compares the lifetime earnings of active-duty military personnel and reservists after retirement. It visualizes key financial elements over time, allowing users to explore different scenarios.

You can visit the functional app at the following link: https://active-vs-reserve-lifetime-earnings.onrender.com/

## Getting Started
Clone the repository, navigate into the folder, and ensure you have the necessary libraries installed. Use the following command to do all three at once (assuming HTTPS):

```bash
git clone https://github.com/JonathanDollahite/ActiveReserveEarningsComparison.git;\
cd DataScienceSalaryPredictor;\
pip install -r requirements.txt
```

After installing the dependencies, run the app with the following command:

```bash
python app.py
```

Visit http://127.0.0.1:8050/ in your web browser to access the app.

## Graph Options:

- **Civilian salary start year:** The year when civilian salary begins.
- **Salary:** Initial civilian salary.
- **Percent yearly raise:** Annual salary increase percentage.
- **Civilian retirement:** The year when civilian retirement starts.

## Output
- The application generates two graphs, one for active-duty personnel and one for reservists, illustrating their respective lifetime earnings trajectories.
- Additionally, the application displays the cumulative lifetime earnings for both scenarios.

## Important Note
Make sure to provide accurate input values for meaningful visualizations. Incorrect inputs may result in inaccurate representations of lifetime earnings.

Feel free to explore and analyze different scenarios to gain insights into the financial aspects of active and reserve military service.
