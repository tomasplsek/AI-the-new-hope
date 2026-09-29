import sys

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def main() -> None:
    x_values = list(range(-10, 11))
    initial_a = 1.0
    initial_b = 0.0
    y_values = [initial_a * (x**2) + initial_b for x in x_values]

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)

    (line,) = ax.plot(x_values, y_values, label="y = A*x^2 + B")
    ax.set_title("Interactive Parabola")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    ax.legend()

    ax_a = plt.axes([0.15, 0.1, 0.7, 0.03])
    ax_b = plt.axes([0.15, 0.05, 0.7, 0.03])

    slider_a = Slider(ax=ax_a, label="A", valmin=-3.0, valmax=3.0, valinit=initial_a)
    slider_b = Slider(ax=ax_b, label="B", valmin=-20.0, valmax=20.0, valinit=initial_b)

    def update(_: float) -> None:
        a_value = slider_a.val
        b_value = slider_b.val
        new_y_values = [a_value * (x**2) + b_value for x in x_values]
        line.set_ydata(new_y_values)
        fig.canvas.draw_idle()

    slider_a.on_changed(update)
    slider_b.on_changed(update)

    if len(sys.argv) > 1:
        fig.savefig(sys.argv[1])
    else:
        plt.show()


if __name__ == "__main__":
    main()
