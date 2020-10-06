from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
import six
from django.utils import timezone
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator


class CustomUserManager(BaseUserManager, models.Manager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        if not email:
            raise ValueError('e-mail is mandatory')

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)

        user.set_password(password)
        print("Usando el safe del CustomUserManager...")
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        print("Creating User custom!!")
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        print("Creating SuperUser custom!!")
        return self._create_user(username, email, password, **extra_fields)


class CustomAbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, email and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'),
    )

    first_name = models.CharField(_('first name'), max_length=30, blank=True)

    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    photo = models.ImageField('Cambiar', upload_to='image_users/',
                              default='image_users/perfil.png', blank=True)

    date_joined = models.DateTimeField(_('Fecha de creación'), default=timezone.now)
    email = models.EmailField('Correo electrónico', max_length=254)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{}, {}'.format(self.last_name, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    get_full_name.short_description = "Full name"

    def __str__(self):
        return self.get_full_name()

    def get_user_image(self):
        if self:
            return format_html("<img style='width:50px;' src='{}'/>".format(self.photo.url))
        else:
            return format_html("<img style='width:50px;' src='images_users/'")

    get_user_image.short_description = "Foto Social"

    class Meta:
        abstract = True
        verbose_name = _('usuario')
        verbose_name_plural = _('ususarios')


class CustomUser(CustomAbstractUser):
    """
        Agregar al usuario el tipo de usuario.
    """

    ADMIN = 1
    TECH = 2
    OPERATOR = 3
    REVIEWER = 4

    USERS_TYPE = [
        (ADMIN, 'Administrador'),
        (TECH, 'Técnico'),
        (OPERATOR, 'Operador'),
        (REVIEWER, 'Revisor'),
    ]

    user_type = models.IntegerField('Tipo de Usuario', choices=USERS_TYPE, default=REVIEWER)

    #TODO: CAMBIAR CONTEST POR REPAIRSHEETS
    '''
    def my_contest(self):
        if self.user_type == CustomUser.TECH:
            return self.contests_accounting.all()
        elif self.user_type == CustomUser.OPERATOR:
            return self.contests_operator.all()
        elif self.user_type == CustomUser.REVIEWER:
            return self.contests_reviewer.all()
        elif self.user_type == CustomUser.ADMIN:
            return Contest.objects.all()
        else:
            return None
    '''

    def save(self, *args, **kwargs):
        if self.id == None:
            user = super(CustomUser, self).save(*args, **kwargs)
            super(CustomUser, self).save(*args, **kwargs)
            grupo = Group.objects.get(pk=self.user_type)
            self.groups.set([grupo])
            if (self.is_superuser):
                self.is_staff = True
            elif (self.user_type > self.ADMIN):
                self.is_staff = False
        self.groups.set([Group.objects.get(pk=self.user_type)])
        super(CustomUser, self).save(*args, **kwargs)
