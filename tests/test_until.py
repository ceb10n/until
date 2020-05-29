from until import Until


class TestUntil:

    def test_tried_times(self):
        until = Until(retry_times=10)
        until(lambda: 1/0)()

        assert until.tried_times == 10

    def test_on_raise(self):
        x = list()

        until = Until(retry_times=10, on_raise=lambda ex: x.append(1))
        until(lambda: 1/0)()

        assert len(x) == 10

    def test_list_of_actions(self):
        x = list()

        excepts = [
            (ZeroDivisionError, lambda ex: x.append(1)),
            (ValueError, lambda ex: print('ValueError'))
        ]

        until = Until(retry_times=10, on_raise=excepts)
        until(lambda: 1/0)()

        assert len(x) == 10

    def test_with_retry_times_zero(self):
        until = Until()
        return_val = until(lambda: 10)()

        assert return_val == 10
        assert until.tried_times == 1

    def test_without_exceptions(self):
        until = Until(retry_times=10)
        return_val = until(lambda: 10)()

        assert return_val == 10
        assert until.tried_times == 1
