# proiect-tw

# 1 for sample data creation

```$python manage.py create_sample data```

# routes for get requests

 + <strong>root</strong> -> app landing page
 + <strong>admin/</strong> -> admin panel
 + <strong>posts/</strong> -> lists all posts
 + posts/post_id={your_post_id}/ -> view a certain post based on it's id
 + author/user_id={your_user_id}/posts/ -> view all the posts of a certain user by it's id
 + author/user_id={your_user_id}/post_id={your_post_id}/ -> view x user's y post
 + skills/skill_id={your_skill_id}/offered/ -> view all posts that offer a certain skill
 + skills/skill_id={your_skill_id}/needed/ -> view all posts that need a certain skill
 + accounts/
 + accounts/
