#include <fstream>
#include <string>
#include <iostream>
#include <utility>
#include <map>
#include <forward_list>
#include <stack>
#include <cassert>

/*
A sequence of current heads, which are each just x,y coordinates.

Every transition, note the "door", which becomes a path on a DAG.
And note every "seen" coordinate, which are the vertices in the DAG.
*/

using Point = std::pair<int, int>;

inline void get_increment(const char dir, char* pdx, char* pdy)
{
  switch (dir)
  {
      case 'W':
        *pdx = -1;
        *pdy = 0;
      break;
      case 'E':
        *pdx = 1;
        *pdy = 0;
      break;
      case 'N':
        *pdx = 0;
        *pdy = -1;
      break;
      case 'S':
        *pdx = 0;
        *pdy = 1;
      break;
      default:
        assert(false);
  }
}

struct ExpInfo
{
public:
  std::forward_list<std::forward_list<Point>*>* alternates;
  std::forward_list<Point>* heads;
};

int main ()
{
  std::fstream input("advent20-1.txt", std::ios::in);
  char ch;
  // ^E(NNN|)
  // (E|W)(NN|SS)
  //     2
  // (E|W)NNN(E(N|W)E)W
  // (1|1)222(1 1|1)2)4
  // E(E|N)N
  // 1(1|1)2

  std::stack<ExpInfo*> depth_stack;

  auto heads = new std::forward_list<Point>({std::make_pair(0, 0)});
  auto next_heads = new std::forward_list<Point>;
  auto alternates = new std::forward_list<std::forward_list<Point>*>;

  std::multimap<Point, Point> edges;
  char dx, dy;

  while (std::char_traits<char>::not_eof(ch = input.get()))
  {
    if (ch == '^' || ch == '$')
    { }
    else if (ch == '(')
    {
      auto info = new ExpInfo();
      info->alternates = alternates;
      info->heads = heads;
      depth_stack.push(info);
      alternates = new std::forward_list<std::forward_list<Point>*>;
      heads = new std::forward_list<Point>({std::make_pair(0, 0)});
    }
    else if (ch == ')')
    {
      alternates->push_front(heads);

      // Pop depth_stack, merge current alternates into previous ones.
      ExpInfo* parent_info = depth_stack.top();
      depth_stack.pop();
      next_heads->clear();

      for (auto parent_head : *parent_info->heads)
      {
        for (auto alternate_heads : *alternates)
        {
          for (auto my_head : *alternate_heads)
          {
            next_heads->emplace_front(
              parent_head.first + my_head.first,
              parent_head.second + my_head.second);
          }

          delete alternate_heads;
        }
      }

      delete alternates;
      heads = next_heads;
      next_heads = new std::forward_list<Point>;
      alternates = parent_info->alternates;
      delete parent_info->heads;
      delete parent_info;
    }
    else if (ch == '|')
    {
      alternates->push_front(heads);
      heads = new std::forward_list<Point>({std::make_pair(0, 0)});
    }
    else if (ch == '\n')
    { }
    else
    {
      get_increment(ch, &dx, &dy);
      next_heads->clear();

      for (auto point : *heads)
      {
        Point successor = std::make_pair(point.first + dx, point.second + dy);
        std::cout << successor.first << " " << successor.second << std::endl;
        edges.insert({point, successor});
        next_heads->push_front(successor);
      }

      std::swap(heads, next_heads);
    }
  }

  int ct = 0;
  for (auto g : *heads)
    ct++;
  std::cout << "head count = " << ct << std::endl;

  return 0;
}
