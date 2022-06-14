from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.template import loader
from queue import PriorityQueue 
import json
from django.shortcuts import redirect

@csrf_exempt

def a_star(source, destination, GRAPH,straight_line):

    p_q,visited = PriorityQueue(),{}
    p_q.put((straight_line[source], 0, source, [source]))
    visited[source] = int(straight_line[source])
    while not p_q.empty():
        (heuristic, cost, vertex, path) = p_q.get()
        print('Queue Status:',heuristic, cost, vertex, path)
        if vertex == destination:
           return heuristic, cost, path
        for next_node in GRAPH[vertex].keys():
            current_cost = cost + int(GRAPH[vertex][next_node])
            heuristic = current_cost + int(straight_line[next_node])
            if not next_node in visited or visited[next_node] >= heuristic:
                visited[next_node] = heuristic
                p_q.put((heuristic, current_cost, next_node,path + [next_node]))


def index(request):
    template = loader.get_template('polls/app.html')
    data = {}
    if request.GET.get('data', None) is not None:
         print('Entered')

        #  print('>>', json.loads(request.GET.get('t')))
         data = request.GET.get('data')
         graph = request.GET.get('graph')
         start = request.GET.get('start')
         end = request.GET.get('end')
         straight =json.loads(data)
         theGraph =json.loads(graph)
         print('>>> ', start,end,theGraph,straight)
         if start not in theGraph or end not in theGraph:
            print('CITY DOES NOT EXIST.')
            return HttpResponse('false')
         else:
            heuristic, cost, optimal_path = a_star(start, end, theGraph, straight)
            print('min of total heuristic_value =', heuristic)
            print('total min cost =', cost)
            print('\nRoute:')
            print(' -> '.join(city for city in optimal_path))
            return HttpResponse(cost)
    return HttpResponse(template.render({}, request))