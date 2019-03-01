import requests


name = "test_drink"

ingredients = [
    {
        'ref': 'd0880c05-5f64-4d3b-ad3c-56f0c4b58e61',
        'measure': 1,
    },
    {
        'ref': 'd0880c05-5f64-4d3b-ad3c-56f0c4b58e61',
        'measure': 1,
    },
    {
        'ref': 'd0880c05-5f64-4d3b-ad3c-56f0c4b58e61',
        'measure': 1,
    },
]

r = requests.post('/api/drinks/', json={'name': 'd1', 'ingredients': [{'ref': self.i1, 'measure': 10}, {'ref': self.i2, 'measure': 20}]})

print(r.status_code)
print(r)
