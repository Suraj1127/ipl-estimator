# IPL Estimator
Calculates the probability that each team makes into playoffs by recursively playing all the games and seeing all the
result possibilities.

## Assumption (Tie Case)

In case of ties that happen when more than one team have equal points and are fighting for top 4 positions, I have
assumed equal probability of making into playoffs for all the tied teams and so incorporated equal weightage.

Example:

If both SRH and MI are on 14 points standing 4th and 5th, I assume probability of them making into playoffs as 0.5
    (for both).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3 (Interpreter)
* Numpy
* Pandas
* Matplotlib
* Seaborn

### Installation
Assuming you have `Python 3` and `pip3`,
```
pip3 install numpy
pip3 install pandas
pip3 install matplotlib
pip3 install seaborn
```

## Usage

With all the requirements fulfilled, run the module `playoff_estimator.py`.

## Authors

* **Suraj Regmi** - *Initial work* - [Suraj](https://github.com/suraj1127)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

